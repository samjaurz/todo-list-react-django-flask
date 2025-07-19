import {TrashIcon, PencilIcon, CheckIcon, XMarkIcon} from "@heroicons/react/24/solid";
import {useState} from "react";

interface Task {
    id: number;
    name: string;
    status: boolean;
}

interface Props {
    task: Task;
    isEditing: boolean;
    onEdit: (task: Task) => void
    onSave: (task: Task) => void
    setEditingId: CallableFunction
    onDelete: (task: Task) => void
    handleCancel: CallableFunction;
}

const TaskRow = ({task, isEditing, onEdit, onSave, onDelete, handleCancel}: Props) => {

    const [value, setValue] = useState(task.name);
    const [statusCompleted, setStatusCompleted] = useState("")
    const boolString = statusCompleted === "completed";

    if (isEditing)
        return (
            <tr className="bg-white">
                <td className="text-center p-3 text-gray-400">{task.id}</td>
                <td className="p-3">
                    <input
                        type="text"
                        className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                        placeholder="New task"
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                    />
                </td>
                <td className="text-center p-3 items-center">
                    <select
                        className="border border-gray-300 rounded px-2 py-1 text-sm"
                        value={statusCompleted}
                        onChange={(e) => setStatusCompleted(e.target.value)}
                    >
                        <option value="incomplete">Incomplete</option>
                        <option value="completed">Completed</option>
                    </select>
                </td>
                <td className="text-right p-4">
                    <div className="inline-flex space-x-2">
                        <button className="bg-green-500 hover:bg-green-600 text-white p-2 rounded">
                            <CheckIcon className="h-4 w-4"
                                       onClick={() => onSave({...task, name: value, status: boolString})}/>
                        </button>
                        <button className="bg-red-500 hover:bg-red-600 text-white rounded p-2">
                            <XMarkIcon className="h-4 w-4" onClick={()=>handleCancel(task)}/>
                        </button>
                    </div>
                </td>
            </tr>
        )
    return (

        <tr key={task.id}
            className={`hover:bg-gray-50 text-center p-3 ${task.status ? "bg-amber-50" : "bg-white"}`}>
            <td className="text-center p-3">{task.id}</td>
            <td className="p-3">{task.name}</td>
            <td className="text-center p-3">{task.status ? "Completed" : "Incomplete"}</td>
            <td className="text-right p-3">
                <div className="inline-flex space-x-2">
                    <button className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded">
                        <PencilIcon className="h-4 w-4" onClick={() => onEdit(task)}/>
                    </button>
                    <button className="bg-red-500 hover:bg-red-600 text-white p-2 rounded">
                        <TrashIcon className="h-4 w-4" onClick={() => onDelete(task)}/>
                    </button>
                </div>
            </td>
        </tr>
    )
}
export default TaskRow;