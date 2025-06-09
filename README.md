# Song Recommendation App

## Overview
This project is a Next.js application designed to help users find song recommendations for their Instagram reels. It features a user-friendly interface where users can input their ideas and receive tailored song suggestions.

## Features
- User input area for entering ideas for Instagram reels.
- Display of song recommendations based on user input.
- Validation and sanitization of user input to ensure security and privacy.
- Responsive design using Tailwind CSS.

## Project Structure
```
song-recommendation-app
├── src
│   ├── app
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components
│   │   ├── IdeaInput.tsx
│   │   └── RecommendationList.tsx
│   ├── types
│   │   └── index.ts
│   ├── lib
│   │   ├── validation.ts
│   │   └── constants.ts
│   └── utils
│       └── sanitize.ts
├── public
│   └── assets
├── middleware.ts
├── .env.example
├── .gitignore
├── next.config.js
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd song-recommendation-app
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Open your browser and go to `http://localhost:3000` to view the application.

## Usage
- Enter your idea for an Instagram reel in the input area.
- Click the submit button to receive song recommendations.
- Review the list of recommended songs displayed below the input area.

## Security
This application follows standard privacy practices, including:
- Input validation to prevent malicious data entry.
- Sanitization of user input to mitigate XSS attacks.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.