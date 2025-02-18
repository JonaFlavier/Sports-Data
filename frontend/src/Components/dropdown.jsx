import React, { useEffect } from "react";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

function Dropdown({ options, onSelect }) {
  const [option, setOption] = React.useState(options[0].id); // initial option is first item in array

  // handle user choosing a game from dropdown
  const handleChange = (event) => {
    setOption(event.target.value);
    onSelect(event.target.value);
  };
  

  return (
    <Box sx={{ minWidth: 120 }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Games</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={option}
          label="Games"
          onChange={handleChange}
        >
          {
            options.map((item, index) =>{
              if(item == 0){
                console.log(options);
              }
              console.log(item);
              return <MenuItem key={index} value={item.id}>{item.home_team_name} vs {item.away_team_name} ({item.venue_name})</MenuItem>
            })
          }

        </Select>
      </FormControl>
    </Box>
  );
}

export default Dropdown;
