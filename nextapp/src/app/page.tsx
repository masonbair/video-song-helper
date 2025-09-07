'use client';

import { useState } from 'react';
import IdeaInput from '../components/IdeaInput';
import RecommendationList from '../components/RecommendationList';
import HashtagSongList from '../components/HashtagSongList';
import './globals.css';
import { Hash } from 'crypto';

export default function Home() {
  const [apiResponse, setApiResponse] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleRecommendations = (data: any) => {
    setApiResponse(data);
    setIsLoading(false);
  };
  
  const handleSearchStart = () => {
    setIsLoading(true);
  };

  return (
    <div className="flex flex-col items-center min-h-screen p-4 md:p-8 bg-gray-50">
      <div className="w-full max-w-6xl">
        <header className="mb-8 text-center">
          <h1 className="text-3xl md:text-4xl font-bold mb-2">TikTok Song Finder</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Find trending songs used in TikTok videos by hashtag. Enter any hashtag to discover music that's popular for that topic.
          </p>
        </header>
        
        <IdeaInput 
          onRecommendationsReceived={handleRecommendations} 
          onSearchStart={handleSearchStart}
        />
        
        {isLoading ? (
          <div className="mt-8 w-full max-w-6xl">
            <div className="flex flex-col items-center justify-center py-12">
              <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-[#e30019]"></div>
              <p className="mt-4 text-gray-600">Finding trending songs...</p>
              <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
            </div>
          </div>
        ) : apiResponse && (
          <HashtagSongList
            key={`songlist-${apiResponse.keyword}-${apiResponse.timestamp}`}
            songs={apiResponse?.songs || []}
            keyword={apiResponse?.keyword || ''}
            count={apiResponse?.count || 0}
            timestamp={apiResponse?.timestamp || ''}
          />
        )}
        
        {/* Legacy component - kept for reference
        <RecommendationList
          recommendations={apiResponse?.recommendations || []}
          count={apiResponse?.count || 0}
          token_status={apiResponse?.token_status || ''}
          timestamp={apiResponse?.timestamp || ''}
        /> */}
      </div>
    </div>
  );
}