import { useState } from "react";
import { teamService } from "../../services/api";

export const CreateTeamMemberModal = ({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: () => void;
}) => {
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [hoursWorked, setHoursWorked] = useState("");

  const handleSubmit = async () => {
    console.log("Submit clicked", { name, role, hoursWorked });

    if (!name || !role || !hoursWorked) return;

    try {
      await teamService.addTeamMember(name, role, parseInt(hoursWorked));
      alert("Team member added successfully.");
      onCreated();
      onClose();
    } catch (error) {
      console.error("Error adding team member:", error);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 p-6 rounded shadow-md w-full max-w-md">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">
          Add Team Member
        </h2>

        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="text"
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="number"
          placeholder="Hours Worked"
          value={hoursWorked}
          onChange={(e) => setHoursWorked(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <div className="flex justify-end space-x-2">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm bg-gray-300 dark:bg-gray-600 rounded"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={!name || !role || !hoursWorked}
            className={`px-4 py-2 text-sm text-white rounded ${
              !name || !role || !hoursWorked
                ? "bg-blue-300 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};
