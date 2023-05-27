import logo from './logo.svg';
import './App.css';
//import {useState} from "react";
import {createTheme} from "@mui/system";
import Grid from "@mui/material/Grid";
import NewItemDialog from "./components/NewItemDialog";
import InventoryTable from "./components/InventoryTable";
import ExistingItemDialog from "./components/ExistingItemDialog";
import { useState, useEffect } from 'react';

const theme = createTheme();
const buttonGridStyle = {
  marginTop: theme.spacing(2),
  marginBottom: theme.spacing(2),
}

const textFieldStyle = {
  marginTop: theme.spacing(2),
  minWidth: "60%"
}

const iconStyle = {
  marginTop: theme.spacing(0.25),
  marginLeft: theme.spacing(0.5),
  marginRight: theme.spacing(0.5),
}

const tableStyle = {
  marginTop: theme.spacing(2),
  width: "75%",
}

function App() {
  const [inventory, setInventory] = useState([]);
  const [selectedItem, setItem] = useState([]);
  const [dialogExisting, setDialogExisting] = useState(false);
  const [readOnly, setReadOnly] = useState(false);

  // useEffect(() => {
  //   console.log("inventory:", inventory);
  // }, [inventory]);

  // useEffect(() => {
  //   console.log("selectedItem:", selectedItem);
  // }, [selectedItem]);

  function deleteItem(id) {
    // Filter out the item with the given id
    console.log("Deleting item with id:", id );
    setInventory(inventory.filter((item) => item.id !== id));
  }

  function editItem(id) {
    setReadOnly(false);
    setItem(inventory.filter((item) => item.id === id));
    setDialogExisting(true);
  } 

  function viewItem(id) {
    setReadOnly(true);
    setItem(inventory.filter((item) => item.id === id));
    setDialogExisting(true);
  }

  function updateItem(id) {
    let existingData = inventory.filter((item) => item.id !== id);
    setInventory([...existingData, ...selectedItem]);
    setDialogExisting(false);
  }

  function toggleDialogExisting() {
    setDialogExisting(false);
    setItem([]);
  }

  return (
    <Grid container justifyContent="center" alignItems="center">
      <NewItemDialog
        iconStyle={iconStyle}
        textFieldStyle={textFieldStyle}
        buttonGridStyle={buttonGridStyle}
        inventory={inventory}
        setInventory={setInventory}
      />
      <ExistingItemDialog 
        textFieldStyle={textFieldStyle}
        buttonGridStyle={buttonGridStyle}
        dialogExisting={dialogExisting} 
        toggleDialogExisting={toggleDialogExisting}
        setItem={setItem}
        selectedItem={selectedItem} 
        readOnly={readOnly} 
        updateItem={updateItem}
      />
      <InventoryTable tableStyle={tableStyle} inventory={inventory} deleteItem={deleteItem} editItem={editItem} viewItem={viewItem} />
    </Grid>
  );
}

export default App;
