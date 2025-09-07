/**
 * API utilities for making requests to the backend
 */

// Determine the API base URL based on the environment
export const getApiBaseUrl = () => {
  // First try to get it from Next.js runtime config
  if (typeof window !== 'undefined') {
    // We're in the browser
    return process.env.NEXT_PUBLIC_API_URL || 
           window.location.protocol + '//' + window.location.hostname + ':8000';
  }
  
  // Server-side
  return process.env.CUSTOM_API_URL || 'http://localhost:8000';
};

/**
 * Fetch data from the API with proper error handling
 */
export async function fetchFromApi(endpoint: string, options = {}) {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
    mode: 'cors' as RequestMode,
  };
  
  try {
    const response = await fetch(url, {
      ...defaultOptions,
      ...options,
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}
