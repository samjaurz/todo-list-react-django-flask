import { TrashIcon, PencilIcon } from "@heroicons/react/24/solid";
import api from "@/lib/axios"
import { useEffect, useState } from "react";

type Task = {
    id: number;
    name: string;
    status: boolean;
};

type Props = {
    tasks: Task[]; 
    task: Task;
    onSelectTask: CallableFunction;
    updateTasks: CallableFunction;
    selectTask: [Task]
};

const BartTask = ({
    tasks,
    updateTasks,

}: Props) => {
  const [formData, setFormData] = useState(tasks);
  const [localTask, setLocalTask] = useState(null);

    const onDeleteTask = async (task: Task)=> {
        console.log("Deleting task", task.id)
        const response = await api.delete(`/task/${task.id}`);
        console.log(response)
        const filteredTasks = tasks.filter(el => el.id != task.id); 
        updateTasks(filteredTasks)
    }

    const postTask = async ()=> {
      if (!localTask) return;
      const payload = {
        name: localTask.name,
        status: localTask.status
      };
      const response = await api.post('/task', payload);
      const newTasks = [
        ...tasks.filter(t => !t.editable),
        {
          id: response.data.id,
          name: response.data.name,
          status: response.data.status
        }
      ];
      updateTasks(newTasks);
      setLocalTask(null); // limpiamos el local
    } 
    
    const onSelectLocalTask = (task)=> {
      console.log("click", task)
      task.editable = true
      setLocalTask(task)
    }
    const handleChangeName = (e) => {
      localTask.name = e.target.value 
      setLocalTask(localTask);
      console.log("chanign name")

    }
    //todo bandera para no agregar mas que un registro handler for onChangeEvent

    const TaskRow = ({task}) => {
      //if (selectTask != undefined)
      if (task.editable && localTask && task.id === localTask.id)
          return (
            <tr className="bg-white" key={task.id}>
                  <td className="text-center p-3 text-gray-400">{localTask.id}</td>
                  <td className="p-3">
                    <input
                      type="text"
                      className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                      placeholder="New task"
                      value={localTask.name}
                      onChange={handleChangeName}
                    />
                  </td>
                  <td className="text-center p-3 items-center">
                    <select
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                      value={localTask.status}
                      onChange={() => console.log("le sssss")}
                    >
                      <option value="incompleted">Incompleted</option>
                      <option value="completed">Completed</option>
                    </select>
                  </td>
                  <td className="text-right p-4">
                    <div className="inline-flex space-x-2">
                    <button className="bg-green-500 hover:bg-green-600 text-white p-2 rounded"
                    onClick={() => postTask}>
                      ✓
                    </button>
                    <button className="bg-red-500 hover:bg-red-600 text-white rounded p-2"
                    onClick={() => postTask}>
                      X
                    </button>
                    </div>
                  </td>
                </tr>)
      return (
          <tr key={task.id}
              className="hover:bg-gray-50"> 
              <td className="text-center p-3">{task.id}</td>
              <td className="p-3">{task.name}</td>
              <td className="text-center p-3">{task.status}</td>
              <td className="text-right p-3">
                <div className="inline-flex space-x-2">
                    <button className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded">
                    <PencilIcon className="h-4 w-4" onClick={() => onSelectLocalTask(task)} />
                    </button>
                  <button className="bg-red-500 hover:bg-red-600 text-white p-2 rounded">
                    <TrashIcon className="h-4 w-4" onClick={() => onDeleteTask(task)}/>
                  </button>
                </div>
              </td>
            </tr>
        )
    }

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
        {localTasks.length > 0 ? (
          localTasks.map((task) => <TaskRow key={task.id} task={task} />)
        ) : (
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

export default BartTask;