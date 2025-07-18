"use client"
import React, {useState} from "react";
import {PlusIcon} from "@heroicons/react/24/solid";


interface Task {
    id: number;
    name: string;
    status: boolean;
}

interface Props {
    tasks: Task[];
    handlerAdd: CallableFunction;
    handleSearch: CallableFunction;
    onEdit: CallableFunction;
}

const SearchBar = ({tasks, handlerAdd,handleSearch, onEdit}: Props) => {
    const [searchTask, setSearchTask] = useState<string>("")

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


    const onChange = (e) => {
        setSearchTask(e.target.value);
        console.log("task", tasks)
        handleSearch(searchTask)
    }

    return (
        <div className="w-full border border-gray-300 rounded-md p-2 bg-white shadow-sm flex gap-4 items-center ">
            <input
                type="text"
                className="flex-1 border border-gray-300 rounded px-2 py-1 text-sm p-0.5"
                placeholder="Search Task"
                value={searchTask}
                onChange={onChange}
            />

            <div className="flex space-x-2 items-start ">
                <button className="bg-green-500 hover:bg-green-600 text-white p-2 rounded">
                    <PlusIcon className="h-4 w-4" onClick={addTask}/>
                </button>
            </div>
        </div>
    );
};

export default SearchBar;
