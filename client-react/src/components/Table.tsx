import TaskRow from "@/components/TaskRow";

interface Task {
    id: number;
    name: string;
    status: boolean;
}

interface Props {
    tasks: Task[];
    editingId: number | null;
    onEdit: (task: Task) => void;
    onSave: (task: Task) => void;
    setEditingId: CallableFunction;
    onDelete: (task: Task) => void;
    handleCancel: CallableFunction;
}

const Table = ({tasks, editingId, onEdit, onSave, setEditingId, onDelete, handleCancel}: Props) => {

    return (
        <div className="py-5">
            <table className="w-full">
                <thead className="bg-gray-50 border-b-2 border-gray-200">
                <tr className="text-sm font-semibold tracking-wide text-left">
                    <th className="p-3 text-center">Id</th>
                    <th className="p-3">Task</th>
                    <th className="p-3 text-center">Status</th>
                    <th className="p-3 text-right">Actions</th>
                </tr>
                </thead>
                <tbody>
                {tasks.length > 0 ? (
                    tasks.map((task) => (
                        <TaskRow
                            key={task.id}
                            task={task}
                            isEditing={editingId === task.id}
                            onEdit={onEdit}
                            onSave={onSave}
                            setEditingId={setEditingId}
                            onDelete={onDelete}
                            handleCancel={handleCancel}
                        />)
                    )) : (
                    <tr>
                        <td colSpan={4} className="text-center p-4 text-gray-500">
                            No tasks found.
                        </td>
                    </tr>
                )}
                </tbody>
            </table>
        </div>
    );
}

export default Table;