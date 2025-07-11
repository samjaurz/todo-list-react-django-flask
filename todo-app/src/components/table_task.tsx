import React from "react";
import { TrashIcon, PencilIcon } from "@heroicons/react/24/solid";
import { useState } from "react";
import { addTask, updateTask, deleteTask } from "@/services/taskService";

type Task = {
  id: number;
  name: string;
  status: boolean;
};
type Props = {
  tasks: Task[];
};

const BartTask = ({
  tasks
}: Props) => {

  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editedTaskName, setEditedTaskName] = useState("");
  const [newTaskName, setNewTaskName] = useState("");
  const [newTaskStatus, setNewTaskStatus] = useState("incompleted");
  const statusBool = newTaskStatus === "completed" 
  const [editedTaskStatus, setEditedTaskStatus] = useState("");
  const [showAddRow, setShowAddRow] = useState(true)
  
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
          {showAddRow && (
            <tr className="bg-white">
              <td className="text-center p-3 text-gray-400">–</td>
              <td className="p-3">
                <input
                  type="text"
                  className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                  placeholder="New task"
                  value={newTaskName}
                  onChange={(e) => setNewTaskName(e.target.value)}
                />
              </td>
              <td className="text-center p-3 items-center">
                <select
                  className="border border-gray-300 rounded px-2 py-1 text-sm"
                  value={newTaskStatus}
                  onChange={(e) => setNewTaskStatus(e.target.value)}
                >
                  <option value="incompleted">Incompleted</option>
                  <option value="completed">Completed</option>
                </select>
              </td>
              <td className="text-right p-5">
                <button
                  className="bg-green-500 hover:bg-green-600 text-white p-2 rounded"
                  onClick={async () => {
                    await addTask(newTaskName, statusBool);
                    setNewTaskName("");
                    setNewTaskStatus("incompleted");
                    setShowAddRow(false);
                  }}
                >
                  Submit
                </button>
              </td>
            </tr>
          )}
          {tasks.length > 0 ? (
            tasks.map((task) => (
              <tr
                key={task.id}
                className={`hover:bg-gray-50 ${
                  task.status ? "bg-green-100" : ""
                }`}
              >
                <td className="text-center p-3">{task.id}</td>
                <td className="p-3">
                  {editingTaskId === task.id ? (
                    <input
                      type="text"
                      value={editedTaskName}
                      onChange={(e) => setEditedTaskName(e.target.value)}
                      className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                    />
                  ) : (
                    task.name
                  )}
                </td>

                <td className="text-center p-3">
                  {editingTaskId === task.id ? (
                    <select
                      value={editedTaskStatus}
                      onChange={(e) => setEditedTaskStatus(e.target.value)}
                      className="border border-gray-300 rounded px-2 py-1 text-sm"
                    >
                      <option value="incompleted">Incompleted</option>
                      <option value="completed">Completed</option>
                    </select>
                  ) : task.status === true ? (
                    "Completed"
                  ) : (
                    "Incompleted"
                  )}
                </td>
                <td className="text-right p-3">
                  <div className="inline-flex space-x-2">
                    {editingTaskId === task.id ? (
                      <button
                        className="bg-green-500 hover:bg-green-600 text-white p-2 rounded"
                        onClick={async () => {
                          const updatedStatus =
                            editedTaskStatus === "completed";

                          await updateTask(
                            task.id,
                            editedTaskName,
                            updatedStatus
                          );
                          setEditingTaskId(null);
                        }}
                      >✓
                      </button>
                    ) : (
                      <button
                        className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded"
                        onClick={() => {
                          setEditingTaskId(task.id);
                          setEditedTaskName(task.name);
                          setEditedTaskStatus(
                            task.status ? "completed" : "incompleted"
                          );
                        }}
                      >
                      <PencilIcon className="h-4 w-4" />
                      </button>
                    )}
                    <button
                      className="bg-red-500 hover:bg-red-600 text-white p-2 rounded"
                      onClick={async () => {
                        await deleteTask(task.id);
                      }}
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))
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
};

export default BartTask;
