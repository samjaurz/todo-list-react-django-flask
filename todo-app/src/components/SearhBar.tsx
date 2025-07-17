"use client"
import React from "react";
import { PlusIcon, ArrowPathIcon } from "@heroicons/react/24/solid";
import { searchTask } from "@/services/taskService";

interface Task {
    id: number;
    name: string;
    status: boolean;
}

interface Props {
    tasks: Task[];
    handlerAdd: CallableFunction;
    onEdit: CallableFunction;
}

const SearchBar = ({ tasks, handlerAdd, onEdit}: Props) => {
  const addTask = () => {
    console.log("add row")
    const new_tasks = [{
      id: 0,
      status: false,
      name: ""
    }, ...tasks];

    console.log("new_task added", new_tasks)
    handlerAdd(new_tasks)
    onEdit(new_tasks[0])
  }

   
  return (
    <div className="w-full border border-gray-300 rounded-md p-2 bg-white shadow-sm flex gap-4 items-center ">
      <input
        type="text"
        className="flex-1 border border-gray-300 rounded px-2 py-1 text-sm p-0.5"
        placeholder="Search Task"
        onChange={(e) => {searchTask( e.target.value);
        }}
      />
      
      <div className="flex space-x-2 items-start ">
        <button className="bg-green-500 hover:bg-green-600 text-white p-2 rounded">
          <PlusIcon className="h-4 w-4" onClick={addTask} />
        </button>
        <button className="bg-yellow-500 hover:bg-yellow-600 text-white p-2 rounded">
          <ArrowPathIcon className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
