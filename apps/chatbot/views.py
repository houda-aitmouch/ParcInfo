import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from datetime import datetime
from .core_chatbot import get_chatbot
from .models import ChatbotInteraction
from django.conf import settings

logger = logging.getLogger(__name__)

def is_authorized_for_chatbot(user):
    """Vérifie si l'utilisateur est autorisé à accéder au chatbot"""
    return user.is_superuser or user.groups.filter(name__in=['Super Admin', 'Gestionnaire Informatique', 'Gestionnaire Bureau']).exists()

def chatbot_ui(request):
    """Render chatbot interface with context"""
    if not is_authorized_for_chatbot(request.user):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Vous n'êtes pas autorisé à accéder au chatbot.")
    
    context = {
        'debug_mode': settings.DEBUG,
        'app_version': getattr(settings, 'APP_VERSION', '1.0')
    }
    return render(request, 'chatbot/chatbot_modern.html', context)

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body or '{}')
            # Accept multiple common keys for compatibility: 'query', 'question', 'text'
            raw_query = data.get('query') or data.get('question') or data.get('text') or ''
            query = raw_query.strip() if isinstance(raw_query, str) else ''
            
            if not query:
                return JsonResponse({
                    'response': 'Veuillez poser une question.',
                    'intent': 'validation',
                    'confidence': 0,
                    'source': 'validation',
                    'method': 'validation_error',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Get chatbot instance
            try:
                chatbot = get_chatbot()
            except Exception as e:
                logger.error(f"Failed to get chatbot instance: {e}")
                return JsonResponse({
                    'response': 'Le chatbot n\'est pas disponible actuellement. Veuillez réessayer plus tard.',
                    'intent': 'error',
                    'confidence': 0,
                    'source': 'error',
                    'method': 'initialization_error',
                    'timestamp': datetime.now().isoformat()
                }, status=500)
            
            # Process query with enhanced RAG+LLM
            try:
                result = chatbot.process_query(query)
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                return JsonResponse({
                    'response': 'Une erreur est survenue lors du traitement de votre question. Veuillez réessayer.',
                    'intent': 'error',
                    'confidence': 0,
                    'source': 'error',
                    'method': 'processing_error',
                    'timestamp': datetime.now().isoformat()
                }, status=500)
            
            # Handle new dictionary response format
            if isinstance(result, dict):
                response_text = result.get('response', 'Erreur de traitement')
                intent = result.get('intent', 'unknown')
                entities = result.get('entities', {})
                confidence = result.get('confidence', 0)
                source = result.get('source', 'unknown')
                method = result.get('method', 'hybrid_rag_llm')
            else:
                # Fallback for old string format
                response_text = str(result)
                intent = 'unknown'
                entities = {}
                confidence = 0
                source = 'unknown'
                method = 'legacy_string'
            
            # Save interaction with correct field names
            try:
                ChatbotInteraction.objects.create(
                    session_id=data.get('session_id', 'web_session'),
                    user_query=query,
                    detected_intent=intent,
                    final_response=response_text,
                    sql_attempted=False,
                    sql_results=0,
                    rag_results=1
                )
            except Exception as e:
                logger.warning(f"Failed to save interaction: {e}")
                # Continue without saving interaction
            
            return JsonResponse({
                'response': response_text,
                'intent': intent,
                'entities': entities,
                'confidence': confidence,
                'source': source,
                'method': method,
                'timestamp': datetime.now().isoformat()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON invalide'}, status=400)
        except Exception as e:
            logger.error(f"Chatbot API error: {e}")
            return JsonResponse({'error': 'Erreur interne du serveur'}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_feedback(request):
    """Handle user feedback on chatbot responses"""
    try:
        data = json.loads(request.body or '{}')
        feedback_type = data.get('feedback_type')  # 'positive' or 'negative'
        content = data.get('content', '')
        timestamp = data.get('timestamp', '')
        message_index = data.get('message_index', 0)
        
        # Log the feedback for analysis
        logger.info(f"User feedback: {feedback_type} for response at {timestamp}")
        
        # Convert feedback_type to rating
        rating = 1 if feedback_type == 'positive' else -1
        
        # Save feedback to database
        from .models import ChatbotFeedback
        ChatbotFeedback.objects.create(
            session_id=f"web_session_{datetime.now().strftime('%Y%m%d')}",
            user=request.user if request.user.is_authenticated else None,
            query=f"Feedback on message {message_index}",
            intent_pred=None,
            entities_pred=None,
            intent_final=None,
            entities_final=None,
            rating=rating,
            reward=rating,  # Simple reward based on rating
            response_snippet=content[:500]  # Limit content length
        )
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_export_pdf(request):
    """Export chatbot response to PDF"""
    try:
        data = json.loads(request.body or '{}')
        content = data.get('content', '')
        
        # Try to use reportlab for PDF generation, fallback to text if not available
        try:
            from django.http import HttpResponse
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from io import BytesIO
            
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Add title
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, height - 50, "Rapport ParcInfo")
            
            # Add content
            p.setFont("Helvetica", 12)
            y_position = height - 100
            
            lines = content.split('\n')
            for line in lines:
                if y_position < 50:  # New page if needed
                    p.showPage()
                    y_position = height - 50
                
                # Clean line for PDF
                clean_line = line.replace('**', '').replace('*', '')
                if len(clean_line) > 80:
                    # Wrap long lines
                    words = clean_line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + " " + word) < 80:
                            current_line += " " + word if current_line else word
                        else:
                            p.drawString(50, y_position, current_line)
                            y_position -= 15
                            current_line = word
                    if current_line:
                        p.drawString(50, y_position, current_line)
                        y_position -= 15
                else:
                    p.drawString(50, y_position, clean_line)
                    y_position -= 15
            
            p.showPage()
            p.save()
            
            buffer.seek(0)
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="parcinfo_export_{datetime.now().strftime("%Y%m%d")}.pdf"'
            
            return response
            
        except ImportError:
            # Fallback: return as text file if reportlab is not available
            logger.warning("ReportLab not available, falling back to text export")
            response = HttpResponse(content, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="parcinfo_export_{datetime.now().strftime("%Y%m%d")}.txt"'
            return response
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return JsonResponse({'error': 'Erreur lors de la génération du PDF', 'message': str(e)}, status=500)


@csrf_exempt
def chatbot_status(request):
    """Get chatbot system status"""
    if request.method == 'GET':
        try:
            chatbot = get_chatbot()
            status = chatbot.get_system_status()
            
            return JsonResponse({
                'status': 'healthy',
                'rag_documents': status.get('rag_documents', 0),
                'llm_available': status.get('llm_available', False),
                'models': status.get('ollama_models', []),
                'embedding_model': status.get('embedding_model', 'unknown'),
                'timestamp': status.get('timestamp', datetime.now().isoformat())
            })
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)