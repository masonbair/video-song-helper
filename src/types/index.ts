export interface Idea {
  id: string;
  content: string;
}

export interface Recommendation {
  id: string;
  title: string;
  artist: string;
  genre: string;
  link: string;
}

export interface Props {
  ideas: Idea[];
  recommendations: Recommendation[];
}