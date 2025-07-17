import TaskRow from "@/components/TaskRow";

interface Task {
    id: number;
    name: string;
    status: boolean;
    editable?: boolean;
};
interface Props {
    tasks: Task[]; 
    updateTasks: CallableFunction;
    editingId: number | null;
    onEdit: (task:Task) =>void;
    onSave: (task: Task) => void;
};

const Table = ({ tasks, updateTasks, editingId, onEdit, onSave}: Props) => {

  

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
          tasks.map((task) =>(
            <TaskRow 
            key={task.id} 
            task={task} 
            isEditing={editingId === task.id}
            updateTasks={updateTasks}
            onEdit={onEdit}
            onSave={onSave}
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