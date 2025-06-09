interface RecommendationListProps {
  apiResponse: any;
}

const RecommendationList: React.FC<RecommendationListProps> = ({ apiResponse }) => {
  return (
    <div className="recommendation-list mt-8">
      <h2 className="text-lg font-bold">Song Recommendations</h2>
      {apiResponse ? (
        <div className="bg-gray-100 p-4 rounded-lg">
          <p><strong>Received Idea:</strong> {apiResponse.receivedIdea}</p>
          <p><strong>Timestamp:</strong> {apiResponse.timestamp}</p>
        </div>
      ) : (
        <p className="text-gray-500">Submit an idea to see the response</p>
      )}
    </div>
  );
};

export default RecommendationList;