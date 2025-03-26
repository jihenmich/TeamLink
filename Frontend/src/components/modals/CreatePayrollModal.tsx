import { useState } from "react";
import { payrollService } from "../../services/api";

export const CreatePayrollModal = ({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: () => void;
}) => {
  const [employeeId, setEmployeeId] = useState("");
  const [salary, setSalary] = useState("");
  const [payrollDate, setPayrollDate] = useState("");
  const [deductions, setDeductions] = useState("");

  const handleSubmit = async () => {
    if (!employeeId || !salary || !payrollDate || !deductions) return;

    try {
      await payrollService.addPayroll(
        employeeId,
        parseFloat(salary),
        payrollDate,
        parseFloat(deductions)
      );
      alert("Payroll entry added successfully.");
      onCreated();
      onClose();
    } catch (error) {
      console.error("Error adding payroll entry:", error);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 p-6 rounded shadow-md w-full max-w-md">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-gray-100">
          Add Payroll Entry
        </h2>

        <input
          type="text"
          placeholder="Employee ID"
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="number"
          placeholder="Salary"
          value={salary}
          onChange={(e) => setSalary(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="date"
          value={payrollDate}
          onChange={(e) => setPayrollDate(e.target.value)}
          className="w-full p-2 mb-3 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
        />

        <input
          type="number"
          placeholder="Deductions"
          value={deductions}
          onChange={(e) => setDeductions(e.target.value)}
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
            disabled={
              !employeeId || !salary || !payrollDate || !deductions
            }
            className={`px-4 py-2 text-sm text-white rounded ${
              !employeeId || !salary || !payrollDate || !deductions
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
