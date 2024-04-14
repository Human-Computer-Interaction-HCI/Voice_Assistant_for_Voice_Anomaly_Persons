import { DatasetRecording } from "@/api/datasets";
import { TableBody } from "@mui/material";
import Table from "@mui/material/Table";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { getLabel } from "./actions";
import { useEffect, useState } from "react";
import Button from "@mui/material-next/Button";

export type RecordingsTableProps = {
    recordings: DatasetRecording[];

}

function LabelCell({ recordingId }: { recordingId: string }) {
    "use client"
    const [label, setLabel] = useState<string>()
    function setLbl() {
        getLabel(recordingId).then(setLabel)
    
    }
    // useEffect(() => {getLabel(recordingId).then(r=>setLabel(r||""))}, [recordingId])
    return <p>{label||<Button onClick={setLbl}>Рапознать</Button>}</p>
}

export default function RecordingsTable({ recordings }: RecordingsTableProps) {
    const columnHelper = createColumnHelper<DatasetRecording>()

    const columns = [
        columnHelper.accessor("label", {
            header: "Метка",
        }),
        columnHelper.accessor("recording_id", {
            header: "Запись"
        }),
        columnHelper.display({
            id: 'recognizedText',
            cell: row => {
                const recordingId = row.row.getValue('recording_id') as string
                return <LabelCell recordingId={recordingId} />
            },
            header: "Распознанная запись"
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