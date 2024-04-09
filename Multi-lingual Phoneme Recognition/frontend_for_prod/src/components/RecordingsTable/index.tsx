import { DatasetRecording } from "@/api/datasets";
import { TableBody } from "@mui/material";
import Table from "@mui/material/Table";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";

export type RecordingsTableProps = {
    recordings: DatasetRecording[];

}

export default function RecordingsTable({ recordings }: RecordingsTableProps) {
    const columnHelper = createColumnHelper<DatasetRecording>()

    const columns = [
        columnHelper.accessor("label", {
            header: "Метка",
        }),
        columnHelper.accessor("recording_id", {
            header: "Запись"
        })
    ]

    const table = useReactTable({ data: recordings, columns, getCoreRowModel: getCoreRowModel() })

    return (
        <div>
            <Table>
                <TableHead>
                    {table.getHeaderGroups().map(headerGroup => (
                        <TableRow key={headerGroup.id}>

                            {headerGroup.headers.map(header => (
                                <TableCell key={header.id}>
                                    {header.isPlaceholder ? null : flexRender(header
                                        .column.columnDef.header, header.getContext()
                                    )}
                                </TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableHead>
                <TableBody>
                    {table.getRowModel().rows.map(row => <TableRow key={row.id}>
                        {row.getVisibleCells().map(cell => <TableCell key={cell.id}>
                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </TableCell>)}
                    </TableRow>)}
                </TableBody>
            </Table>
        </div>
    )

}