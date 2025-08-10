interface Recommendation {
  title: string;
  artist: string;
  genre: string;
  link: string;
}

interface RecommendationListProps {
  recommendations: Recommendation[];
  count: number;
  token_status: string;
  timestamp: string;
}

const RecommendationList: React.FC<RecommendationListProps> = ({ recommendations, count, token_status, timestamp }) => {
  return (
    <div className="recommendation-list mt-8">
      <h2 className="text-lg font-bold">Song Recommendations</h2>
      <div className="bg-gray-100 p-4 rounded-lg mb-4">
        <p><strong>Count:</strong> {count}</p>
        <p><strong>Token Status:</strong> {token_status}</p>
        <p><strong>Timestamp:</strong> {timestamp}</p>
      </div>
      {recommendations.length > 0 ? (
        <ul className="space-y-4">
          {recommendations.map((rec, idx) => (
            <li key={idx} className="border p-4 rounded-lg bg-white shadow">
              <p><strong>Title:</strong> {rec.title}</p>
              <p><strong>Artist:</strong> {rec.artist}</p>
              <p><strong>Genre:</strong> {rec.genre}</p>
              <a href={rec.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">View on TikTok</a>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">Submit an idea to see the response</p>
      )}
    </div>
  );
};

export default RecommendationList;