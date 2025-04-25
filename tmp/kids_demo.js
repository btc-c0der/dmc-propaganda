// Kids Demo Server - No Authentication Required
// Simple Express server to demonstrate campaign & client management
// For educational storytelling session on April 24, 2025

const express = require('express');
const app = express();
const port = 3100;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Demo data
const clients = [
  {
    id: 'client1',
    name: 'Escola Primária Campinas',
    contactPerson: 'Diretora Maria Silva',
    logo: 'school.png',
    description: 'Local primary school for ages 6-12'
  },
  {
    id: 'client2',
    name: 'Festival Cultural Brasil-Espanha',
    contactPerson: 'Carlos Hernández',
    logo: 'festival.png',
    description: 'Annual cultural exchange festival'
  }
];

const campaigns = [
  {
    id: 'camp1',
    name: 'Geography Adventure Day',
    client: 'client1',
    description: 'Interactive map session for 3rd graders',
    startDate: '2025-04-25',
    status: 'active',
    objectives: ['Teach geography', 'Cultural exchange', 'Fun learning'],
    targetAudience: {
      demographics: 'Children 8-9 years',
      interests: ['Maps', 'Travel', 'Other countries'],
    }
  },
  {
    id: 'camp2',
    name: 'Spain-Brazil Friendship Concert',
    client: 'client2',
    description: 'Music showcase featuring traditions from both countries',
    startDate: '2025-05-15',
    status: 'planning',
    objectives: ['Cultural appreciation', 'Music education', 'Community building'],
    targetAudience: {
      demographics: 'All ages',
      interests: ['Music', 'Culture', 'International relations'],
    }
  }
];

// Routes for client operations
app.get('/api/demo/clients', (req, res) => {
  res.json({
    success: true,
    data: clients,
    message: 'Clients retrieved successfully'
  });
});

app.get('/api/demo/clients/:id', (req, res) => {
  const client = clients.find(c => c.id === req.params.id);
  if (!client) {
    return res.status(404).json({
      success: false,
      message: 'Client not found'
    });
  }
  res.json({
    success: true,
    data: client,
    message: 'Client retrieved successfully'
  });
});

// Routes for campaign operations
app.get('/api/demo/campaigns', (req, res) => {
  res.json({
    success: true,
    data: campaigns,
    message: 'Campaigns retrieved successfully'
  });
});

app.get('/api/demo/campaigns/:id', (req, res) => {
  const campaign = campaigns.find(c => c.id === req.params.id);
  if (!campaign) {
    return res.status(404).json({
      success: false,
      message: 'Campaign not found'
    });
  }
  
  // Enhance campaign with client details
  const client = clients.find(c => c.id === campaign.client);
  const enhancedCampaign = {
    ...campaign,
    clientDetails: client
  };
  
  res.json({
    success: true,
    data: enhancedCampaign,
    message: 'Campaign retrieved successfully'
  });
});

// Routes for educational content
app.get('/api/demo/educational', (req, res) => {
  res.json({
    success: true,
    data: {
      title: "Spain to Brazil Explorer",
      description: "Interactive geography game for kids",
      funFacts: [
        "Brazil speaks Portuguese, not Spanish!",
        "Spain is in Europe, Brazil is in South America",
        "A flight from Spain to Brazil takes about 10 hours",
        "The Atlantic Ocean separates Spain and Brazil",
        "Both countries love soccer/football!"
      ],
      activities: [
        {
          name: "Map Explorer",
          description: "Interactive map showing Spain and Brazil",
          path: "/map-explorer"
        },
        {
          name: "Culture Quiz",
          description: "Test your knowledge of both countries",
          path: "/culture-quiz"
        }
      ]
    },
    message: 'Educational content retrieved successfully'
  });
});

// Simple index page for the storytelling session
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>DMC Propaganda - Kids Geography Adventure</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            color: #333;
            background-color: #f0f8ff;
            margin: 0;
            padding: 20px;
            text-align: center;
          }
          h1 {
            color: #4169e1;
          }
          .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
          }
          .button {
            background-color: #4caf50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
            text-decoration: none;
            display: inline-block;
          }
          .map-container {
            border: 2px solid #4169e1;
            border-radius: 8px;
            padding: 10px;
            margin: 20px 0;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Spain to Brazil: Geography Adventure!</h1>
          <h2>Welcome to DMC Propaganda's Kids Storytelling Session</h2>
          <p>Today, April 24, 2025</p>
          
          <div class="map-container">
            <h3>Our Journey Today</h3>
            <p>We'll be exploring the amazing connection between Spain and Brazil through fun stories and activities!</p>
            <p>Get ready to learn about different languages, cultures, and the vast ocean between these two wonderful countries.</p>
          </div>
          
          <div>
            <a class="button" href="/start-story">Start Our Story</a>
            <a class="button" href="/launch-game">Play The Map Game</a>
          </div>
          
          <p style="margin-top: 30px;">DMC Propaganda - Connecting Cultures Through Education</p>
        </div>
      </body>
    </html>
  `);
});

// Route to launch the turtle game
app.get('/launch-game', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Launch Map Game</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            color: #333;
            background-color: #f0f8ff;
            margin: 0;
            padding: 20px;
            text-align: center;
          }
          .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
          }
          .button {
            background-color: #ff6f00;
            color: white;
            padding: 15px 25px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 18px;
            margin: 20px;
            text-decoration: none;
            display: inline-block;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Let's Play the Spain-Brazil Map Game!</h1>
          <p>Click the button below to launch our interactive geography game:</p>
          
          <a class="button" href="#" onclick="launchGame(); return false;">Launch Map Game</a>
          
          <p>You'll learn about:</p>
          <ul style="display: inline-block; text-align: left;">
            <li>Where Spain and Brazil are located</li>
            <li>The journey across the Atlantic Ocean</li>
            <li>Fun facts about both countries</li>
            <li>Languages, culture, and more!</li>
          </ul>
          
          <script>
            function launchGame() {
              alert("This would normally launch our Python turtle game! For the storytelling session, your teacher will show this on the main screen.");
              // In a real implementation, this could use a backend call to launch the Python script
              // Or could embed a web-based version of the game
            }
          </script>
        </div>
      </body>
    </html>
  `);
});

// Start the server
app.listen(port, () => {
  console.log(`Kids Demo server running at http://localhost:${port}`);
  console.log(`Ready for the storytelling session on April 24, 2025!`);
});