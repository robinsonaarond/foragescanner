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

export function setExistingTextField(label, field, item, value, props, changeInfo) {
    return (
        <TextField
            label={label}
            sx={props.textFieldStyle}
            variant="outlined"
            value={value}
            onChange={(e) => changeInfo(item.id, field, e.target.value)}
            InputProps={{readOnly: props.readOnly}}
        ></TextField>
    );
}

export default function ExistingItemDialog(props) {
    function changeInfo(id, field, value) {
        console.log("Going to change item with id:", id, "field:", field, "value:", value);
        const newState = props.selectedItem.map((item) => {
            if (item.id === id && field !== "quantity") {
                return {...item, [field]: value};
            } else {
                return item;
            }
        });
        props.setItem(newState);
    }

    function editQuantity(id, original, amount) {
        const newState = props.selectedItem.map((item) => {
            if (original === 0 && amount === -1) {
                console.log("Unable to subtract from 0");
            } else if (item.id === id) {
                return {...item, quantity: original + amount};
            }
            return item;
        });
        props.setItem(newState);
    }

    return (
        <>
        <Dialog open={props.dialogExisting} onClose={props.toggleDialogExisting}>
            <DialogContent>
                <Grid
                    container
                    direction="column"
                    justifyContent="center"
                    alignItems="center"
                >
                    {props.selectedItem.map((item) => (
                        <div key={item.id}>
                            {setExistingTextField("Name", "name", item, item.name, props, changeInfo)}
                            {setExistingTextField("Description", "description", item, item.description, props, changeInfo)}
                            {setExistingTextField("Location", "location", item, item.location, props, changeInfo)}
                            <Grid sx={props.buttonGridStyle}>
                                {props.readOnly === false && (
                                    <IconButton onClick={() => {
                                        editQuantity(item.id, item.quantity, -1);
                                    }} sx={props.iconStyle}>
                                        <RemoveIcon sx={props.iconStyle} />
                                    </IconButton>
                                )}
                                {props.readOnly === true && "Quantity:"} {item.quantity}
                                {props.readOnly === false && (
                                    <IconButton onClick={() => {
                                        editQuantity(item.id, item.quantity, 1);
                                    }} sx={props.iconStyle}>
                                        <AddIcon sx={props.iconStyle} />
                                    </IconButton>
                                )}
                                <DialogActions>
                                    <Button onClick={props.toggleDialogExisting}>
                                        {props.readOnly === true ? "Close" : "Cancel"}
                                    </Button>
                                    {props.readOnly === false && (
                                        <Button onClick={() => {
                                            props.updateItem(item.id);
                                        }}>Update</Button>
                                    )}
                                </DialogActions>
                            </Grid>
                        </div>
                    ))}
                </Grid>
            </DialogContent>
        </Dialog>
        </>
    )
}