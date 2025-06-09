'use client';

import React from "react";

interface IdeaInputProps {
  onRecommendationsReceived: (recommendations: any) => void;
}

const IdeaInput: React.FC<IdeaInputProps> = ({ onRecommendationsReceived }) => {
  const [idea, setIdea] = React.useState<string>("");
  const [error, setError] = React.useState<string>("");
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setIdea(event.target.value);
    setError("");
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (idea.trim() === "") {
      setError("Please enter an idea for your Instagram reel.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea: idea })
      });
      
      const data = await response.json();
      onRecommendationsReceived(data);
    } catch (err) {
      setError("Failed to fetch recommendations");
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