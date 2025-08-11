import React from "react";

interface HashtagSong {
  title: string;
  artist: string;
  genre?: string;
  link: string;
}

interface HashtagSongListProps {
  songs: HashtagSong[];
  keyword: string;
  count: number;
  timestamp: string;
}

const HashtagSongList: React.FC<HashtagSongListProps> = ({ songs, keyword, count, timestamp }) => {
  return (
    <div className="hashtag-song-list mt-8">
      <h2 className="text-lg font-bold">Songs for #{keyword}</h2>
      <div className="bg-gray-100 p-4 rounded-lg mb-4">
        <p><strong>Count:</strong> {count}</p>
        <p><strong>Timestamp:</strong> {timestamp}</p>
      </div>
      {songs.length > 0 ? (
        <ul className="space-y-4">
          {songs.map((song, idx) => (
            <li key={idx} className="border p-4 rounded-lg bg-white shadow">
              <p><strong>Title:</strong> {song.title}</p>
              <p><strong>Artist:</strong> {song.artist}</p>
              {song.genre && <p><strong>Genre:</strong> {song.genre}</p>}
              <a href={song.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">View on TikTok</a>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">No songs found for this hashtag.</p>
      )}
    </div>
  );
};

export default HashtagSongList;
