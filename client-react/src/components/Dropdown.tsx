import React, {useState} from "react";

interface User {
    id: number,
    name: string,
    last_name: string,
    status: boolean
}

interface Props {
    users: User[];
    handleFilterUser: (userId: number) => void;
}

const Dropdown = ({users, handleFilterUser}: Props) => {
    const [selectedValue, setSelectedValue] = useState('');

    const handleChange =  (event: React.ChangeEvent<HTMLSelectElement>) => {
        const value=event.target.value
        setSelectedValue(value);
        handleFilterUser(parseInt(value))
  };
    return (

        <div>
            <select value={selectedValue} onChange={handleChange}>
                <option value="">Select a user</option>
                {users.map((users) => (
                    <option key={users.id} value={users.id}>
                        {users.name}
                    </option>
                ))}
            </select>
        </div>
    )
};

export default Dropdown;

