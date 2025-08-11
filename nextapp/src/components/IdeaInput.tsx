'use client';

import React from "react";

interface IdeaInputProps {
  onRecommendationsReceived: (recommendations: any) => void;
  onHashtagSongsReceived?: (songsData: any) => void; // optional
}

const IdeaInput: React.FC<IdeaInputProps> = ({ onRecommendationsReceived, onHashtagSongsReceived }) => {
  const [idea, setIdea] = React.useState<string>("");
  const [error, setError] = React.useState<string>("");
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setIdea(event.target.value);
    setError("");
  };

  const fetchTrendingRecommendations = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/tiktok/trending', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }      
      });
      return await response.json();
    } catch (err) {
      throw err;
    }
  };

  const fetchSongsByHashtag = async (hashtag: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/songs/by-hashtag`);
      const data = await response.json();
      if (onHashtagSongsReceived) {
        onHashtagSongsReceived(data);
      }
    } catch (err) {
      setError("Failed to fetch hashtag songs: " + (err instanceof Error ? err.message : "Unknown error"));
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (idea.trim() === "") {
      setError("Please enter an idea for your Instagram reel.");
      return;
    }

    setIsLoading(true);
    try {
      // The API call is called here, depending on what I need to have testing or running
      const data = await fetchSongsByHashtag("travel");
      onRecommendationsReceived(data);
    } catch (err) {
      setError("Failed to fetch recommendations: "+ (err instanceof Error ? err.message : "Unknown error"));
    } finally {
      setIsLoading(false);
    }
    
    setIdea(""); // Clear input after submission
  };

  

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-w-2xl mx-auto p-4">
      <textarea
        value={idea}
        onChange={handleInputChange}
        placeholder="Enter your idea for an Instagram reel"
        className="border p-4 rounded-lg shadow-sm resize-none"
        rows={4}
      />
      {error && <p className="text-red-500">{error}</p>}
      <button 
        type="submit" 
        className="bg-[#e30019] hover:bg-[#a30b18] text-white p-3 rounded-lg transition-all duration-200"
        disabled={isLoading}
      >
        {isLoading ? 'Loading...' : 'Submit Idea'}
      </button>
    </form>
  );
};

export default IdeaInput;