import { useEffect, useState } from "react";
import "./App.css";
import Dropdown from "./Components/dropdown";
import Histogram from "./Components/histogram";

function App() {

  // simple use state
  const [games, setGames] = useState(null); 
  const [currentGame, setCurrentGame] = useState(null);
  const [venues, setVenues] = useState(null);
  const [teams, setTeams] = useState(null);
  const [selected, setSelected] = useState(-1);

  const handleSelected = value => {
    console.log(value);
    setSelected(value);
    setCurrentGame(null); // clear current game data
  }


  // simple use effect
  useEffect(() => {
    // load all venues, teams and games
    const fetchData = async () => {
      try {
        // fetch both venues and teams data
        const [venues_resp, teams_resp, games_resp] = await Promise.all([
          fetch('http://localhost:80/venues'),
          fetch('http://localhost:80/teams'),
          fetch('http://localhost:80/games'),
        ]);

        // Parse JSON responses in parallel
        const [venues_data, teams_data, games_data] = await Promise.all([venues_resp.json(), teams_resp.json(), games_resp.json()]);

        // set venues, teams and games data
        setVenues(venues_data);
        setTeams(teams_data);
        setGames(games_data);
        // fetch the first data for first histogram
        setSelected(games_data[0].id);
      
        console.log(venues_data);
        console.log(teams_data);
        console.log(games_data);

      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
    // fetchGameData(6);

  }, [])

  useEffect(() => {
    if(selected>-1){
      fetchGameData(selected);
    }
  }, [selected])
  




  const fetchGameData = async (game_id) => {

    try {
      // fetch both venues and teams data
      const [games_resp] = await Promise.all([
        fetch('http://localhost:80/games',{
          method: 'POST', // Specify the HTTP method
          headers: {
              'Content-Type': 'application/json' // Tell the server you're sending JSON
          },
          body: JSON.stringify({
            'game_id': game_id
          }) // Convert JavaScript object to JSON string
        }),
      ]);

      // Parse JSON responses in parallel
      const [games_data] = await Promise.all([games_resp.json()]);

      // format game to display simulation results
      setCurrentGame(games_data.data);
      console.log(games_data.data);
    } catch (error) {
      console.error(error);
    }

  }

    
  



  return (

    <div className="App">
      <header className="App-header">
        {
          games && <Dropdown options={games} onSelect={handleSelected} />
        }
      
      {currentGame ? (
                
                    <Histogram title={`${currentGame.game_date}`} data={currentGame} />
                
            ) : (
                <p>Data Loading ...</p>
            )}
      </header>

      
    </div>
  );
}

export default App;
