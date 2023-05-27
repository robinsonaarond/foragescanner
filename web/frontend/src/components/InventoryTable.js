import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    IconButton,
} from "@mui/material"
import {
    Edit as EditIcon,
    DeleteForever as DeleteIcon,
} from "@mui/icons-material";

const TableCellStyle = {
    color: "white",
    fontWeight: "bold",
}

function myTableCell(cellName) {
    return (
        <TableCell sx={TableCellStyle} align="right">
            {cellName}
        </TableCell>
    );
}

export default function InventoryTable(props) {
    return  <>
    {props.inventory.length > 0 && (
        <TableContainer sx={props.tableStyle} component={Paper}>
            <Table>
                <TableHead sx={{backgroundColor: "#ffc107"}}>
                    <TableRow>
                        {myTableCell("Name")}
                        {myTableCell("Quantity")}
                        {myTableCell("Location")}
                        <TableCell align="right"></TableCell>
                        <TableCell align="right"></TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {props.inventory.map((row) => (
                        <TableRow hover key={row.name}>
                            <TableCell onClick={() => {props.viewItem(row.id)}} align="right">{row.name}</TableCell>
                            <TableCell onClick={() => {props.viewItem(row.id)}} align="right">{row.quantity}</TableCell>
                            <TableCell onClick={() => {props.viewItem(row.id)}} align="right">{row.location}</TableCell>
                            <TableCell align="right">
                                <IconButton onClick={() => {props.editItem(row.id)}}>
                                    <EditIcon />
                                </IconButton>
                            </TableCell>
                            <TableCell align="right">
                                <IconButton onClick={() => {props.deleteItem(row.id)}}>
                                    <DeleteIcon />
                                </IconButton>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    )}
    </>;
}