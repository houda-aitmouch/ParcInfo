import { clsx, type ClassValue } from "clsx";

export function cn(...inputs: ClassValue[]) {
  // Simple class name joiner without tailwind-merge
  return clsx(inputs);
}
