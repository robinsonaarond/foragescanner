import {useState} from "react";
import {
    Grid, 
    Button, 
    Dialog, 
    DialogContent, 
    DialogActions,
    TextField,
    IconButton,
} from "@mui/material";
import {Add as AddIcon, DataArrayOutlined, Remove as RemoveIcon} from "@mui/icons-material";

export function setTextField(label, name, setFunction, props) {
    return (
        <TextField 
            label={label}
            sx={props.textFieldStyle} 
            variant="outlined" 
            value={name} 
            onChange={(e) => setFunction(e.target.value)}
        ></TextField>
    );
}

export default function NewItemDialog(props) {
    const [dialogNew, setDialogNew] = useState(false);
    const [name, setName] = useState("");
    const [quantity, setQuantity] = useState(0);
    const [description, setDescription] = useState("");
    const [location, setLocation] = useState("");

    function toggleDialogNew() {
        setDialogNew(!dialogNew);
        clearAll();
    }

    function changeQuantity(amount) {
        if (quantity === 0 && amount === -1) {
            return null;
        }
        setQuantity(quantity + amount);
    }

    function clearAll() {
        setName("");
        setQuantity(0);
        setDescription("");
        setLocation("");
    }

    function addItem() {
        let array = [];
        array.push({
            id: props.inventory.length + 1,
            name, 
            description, 
            location,
            quantity
        });
        toggleDialogNew();
        props.setInventory([...props.inventory, ...array]);
        console.log("inv arr:", array);
    }

    return (
    <Grid container direction="column" justifyContent="center" alignItems="center">
        <Button 
            variant="contained" 
            sx={props.buttonGridStyle} 
            onClick={toggleDialogNew}
        >Add</Button>
        <Dialog open={dialogNew} onClose={toggleDialogNew}>
            <DialogContent>
                {setTextField("Name", name, setName, props)}
                {setTextField("Description", description, setDescription, props)}
                {setTextField("Location", location, setLocation, props)}
                <Grid sx={props.buttonGridStyle}>
                    <IconButton onClick={() => {changeQuantity(-1)}} sx={props.iconStyle}><RemoveIcon /></IconButton>
                    {quantity}
                    <IconButton onClick={() => {changeQuantity(1)}} sx={props.iconStyle}><AddIcon /></IconButton>
                </Grid>
                <DialogActions>
                    <Button onClick={toggleDialogNew}>Cancel</Button>
                    <Button onClick={addItem} >Add</Button>
                </DialogActions>
            </DialogContent>
        </Dialog>
    </Grid>
    );
}