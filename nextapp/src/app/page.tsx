'use client';

import { useState } from 'react';
import IdeaInput from '../components/IdeaInput';
import RecommendationList from '../components/RecommendationList';
import HashtagSongList from '../components/HashtagSongList';
import './globals.css';
import { Hash } from 'crypto';

export default function Home() {
  const [apiResponse, setApiResponse] = useState<any>(null);

  const handleRecommendations = (data: any) => {
    setApiResponse(data);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-4">Song Recommendation App</h1>
      <IdeaInput onRecommendationsReceived={handleRecommendations} />
      <HashtagSongList
        songs={apiResponse?.songs || []}
        keyword={apiResponse?.keyword || ''}
        count={apiResponse?.count || 0}
        timestamp={apiResponse?.timestamp || ''}
      />
      {/* <RecommendationList
        recommendations={apiResponse?.recommendations || []}
        count={apiResponse?.count || 0}
        token_status={apiResponse?.token_status || ''}
        timestamp={apiResponse?.timestamp || ''}
      /> */}
    </div>
  );
}