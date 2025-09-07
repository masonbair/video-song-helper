'use client';

import React from "react";
import { fetchFromApi } from "../utils/api";

interface IdeaInputProps {
  onRecommendationsReceived: (recommendations: any) => void;
  onHashtagSongsReceived?: (songsData: any) => void; // optional
  onSearchStart?: () => void; // New prop to signal search started
}

const IdeaInput: React.FC<IdeaInputProps> = ({ 
  onRecommendationsReceived, 
  onHashtagSongsReceived,
  onSearchStart
}) => {
  const [hashtag, setHashtag] = React.useState<string>("");
  const [error, setError] = React.useState<string>("");
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // Remove any # symbol if the user adds it
    setHashtag(event.target.value.replace(/^#/, ''));
    setError("");
  };

  const fetchTrendingRecommendations = async () => {
    try {
      return await fetchFromApi('api/tiktok/trending');
    } catch (err) {
      throw err;
    }
  };

  const fetchSongsByHashtag = async (hashtag: string) => {
    try {
      // Use our API utility to make the request
      return await fetchFromApi(`api/songs/by-hashtag?keyword=${encodeURIComponent(hashtag)}`);
    } catch (err) {
      setError("Failed to fetch hashtag songs: " + (err instanceof Error ? err.message : "Unknown error"));
      throw err;
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (hashtag.trim() === "") {
      setError("Please enter a hashtag to search for.");
      return;
    }

    setIsLoading(true);
    // Notify parent component that search has started
    if (onSearchStart) {
      onSearchStart();
    }
    
    try {
      // Call the API with the user-provided hashtag
      const data = await fetchSongsByHashtag(hashtag.trim());
      onRecommendationsReceived(data);
    } catch (err) {
      setError("Failed to fetch songs: "+ (err instanceof Error ? err.message : "Unknown error"));
      setIsLoading(false); // Reset loading state on error
    }
  };

  

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-w-2xl mx-auto p-4 w-full">
      <div className="mb-4">
        <label htmlFor="hashtag" className="block text-sm font-medium text-gray-700 mb-1">
          Enter a hashtag to find TikTok songs:
        </label>
        <div className="flex">
          <span className="inline-flex items-center px-3 text-sm text-gray-500 bg-gray-100 border border-r-0 border-gray-300 rounded-l-md">
            #
          </span>
          <input
            id="hashtag"
            type="text"
            value={hashtag}
            onChange={handleInputChange}
            placeholder="travel, food, dance, etc."
            className="flex-1 border p-4 rounded-r-lg shadow-sm"
          />
        </div>
      </div>
      
      {error && <p className="text-red-500">{error}</p>}
      <button 
        type="submit" 
        className="bg-[#e30019] hover:bg-[#a30b18] text-white p-3 rounded-lg transition-all duration-200"
        disabled={isLoading}
      >
        {isLoading ? 'Searching...' : 'Find Songs'}
      </button>
    </form>
  );
};

export default IdeaInput;