import React, { useState, useRef, useEffect } from "react";

interface HashtagSong {
  title: string;
  author: string;
  id: string;
  play_url: string;
  cover_url: string;
  duration: number;
  video_url: string;
}

interface HashtagSongListProps {
  songs: HashtagSong[];
  keyword: string;
  count: number;
  timestamp: string;
}

const defaultCover = "https://placehold.co/600x600/e8e8e8/a3a3a3?text=No+Cover&font=montserrat";

const SongCard: React.FC<{ song: HashtagSong, idx: number }> = ({ song, idx }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);
  const [audioKey, setAudioKey] = useState(`${song.id || idx}-${Date.now()}`);
  
  // Effect to reset player when the song changes
  useEffect(() => {
    // Stop any playing audio and reset state when song changes
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
    // Force audio element to recreate by changing its key
    setAudioKey(`${song.id || idx}-${Date.now()}`);
  }, [song.id, song.play_url, song.title, idx]);

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play().catch(e => {
          console.error("Error playing audio:", e);
        });
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <li 
      className="relative rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-all h-40 group aspect-square"
    >
      {/* Cover Image - Fixed size with consistent aspect ratio */}
      <div 
        className="absolute inset-0 bg-cover bg-center h-full w-full" 
        style={{ 
          backgroundImage: `url(${song.cover_url || defaultCover})`,
          filter: 'brightness(0.7)',
          backgroundSize: 'cover',
          aspectRatio: '1 / 1'
        }}
        onError={(e) => {
          // Fallback to default cover if image fails to load
          (e.target as HTMLElement).style.backgroundImage = `url(${defaultCover})`;
        }}
      />
      
      {/* Dark overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-40 transition-opacity group-hover:bg-opacity-30" />
      
      {/* Content */}
      <div 
        className="relative z-10 flex flex-col justify-between h-full p-4 text-white cursor-pointer"
        onClick={togglePlay}
      >
        <div>
          <h3 className="font-bold text-sm text-white mb-1 line-clamp-1">{song.title}</h3>
          <p className="text-gray-200 text-xs line-clamp-1">{song.author}</p>
          
          {/* Play/Pause Icon */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 opacity-70 group-hover:opacity-100 transition-all">
            {isPlaying ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6m-7-8a1 1 0 011-1h8a1 1 0 011 1v10a1 1 0 01-1 1H8a1 1 0 01-1-1V9z" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            )}
          </div>
        </div>
        
        <div>
          {/* Bottom Info Bar */}
          <div className="flex justify-between items-center">
            {song.duration > 0 && (
              <span className="text-sm opacity-75">
                {Math.floor(song.duration / 60)}:{(song.duration % 60).toString().padStart(2, '0')}
              </span>
            )}
            <a 
              href={song.video_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-white hover:underline bg-black bg-opacity-50 px-2 py-1 rounded-full text-xs"
              onClick={(e) => e.stopPropagation()}
            >
              TikTok
            </a>
          </div>
        </div>
      </div>
      
      {/* Hidden audio player */}
      {song.play_url && (
        <audio 
          ref={audioRef}
          key={audioKey}
          className="hidden"
          onEnded={() => setIsPlaying(false)}
          preload="none"
        >
          <source src={song.play_url} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      )}
    </li>
  );
};

const HashtagSongList: React.FC<HashtagSongListProps> = ({ songs, keyword, count, timestamp }) => {
  return (
    <div className="hashtag-song-list mt-8 w-full max-w-6xl">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Songs for #{keyword}</h2>
        <div className="text-sm text-gray-500">
          <span>{count} songs found • </span>
          <span>{new Date(timestamp).toLocaleString()}</span>
        </div>
      </div>
      
      {songs.length > 0 ? (
        <ul className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 auto-rows-fr"
            key={`songlist-${keyword}-${timestamp}`}
        >
          {songs.map((song, idx) => (
            <SongCard key={`song-${idx}-${song.id}-${timestamp}`} song={song} idx={idx} />
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">No songs found for this hashtag.</p>
      )}
    </div>
  );
};

export default HashtagSongList;
