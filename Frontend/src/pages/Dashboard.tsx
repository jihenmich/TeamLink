import { useEffect, useState } from 'react';
import { teamService, leaveService, payrollService, timeTrackingService } from '../services/api';
import { CreateLeaveModal } from '../components/modals/CreateLeaveModal';
import { CreateTeamMemberModal } from '../components/modals/CreateTeamMemberModal';
import { CreatePayrollModal } from '../components/modals/CreatePayrollModal';
import { CreateTimeTrackingModal } from '../components/modals/CreateTimeTrackingModal';


interface TeamMember {
  id: string;
  name: string;
  role: string;
  hoursWorked: number;
}

interface DashboardData {
  teamMembers: TeamMember[];
  leaveRequests: {
    id: string;
    employeeId?: string | number;
    startDate?: string;
    endDate?: string;
    status: string;
  }[];
  payroll: {
    id: string;
    employeeId?: string | number;
    salary: number;
    payrollDate: string;
    deductions: number;
  }[];
  timeTracking: {
    id: string;
    employeeId?: string | number;
    clockIn: string;
    clockOut: string;
    totalHours: number;
  }[];
}

export const Dashboard = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [showLeaveModal, setShowLeaveModal] = useState(false);
  const [showTeamModal, setShowTeamModal] = useState(false);
  const [showPayrollModal, setShowPayrollModal] = useState(false);
  const [showTimeTrackingModal, setShowTimeTrackingModal] = useState(false);

  const fetchDashboardData = async () => {
    try {
      const [teamResponse, rawLeave, rawPayroll, rawTimeTracking] = await Promise.all([
        teamService.getTeamMembers(),
        leaveService.getAllLeaveRequests(),
        payrollService.getAllPayrollData(),
        timeTrackingService.getAllTimeTracking(),
      ]);

      const leaveResponse = rawLeave.map((item: any) => ({
        ...item,
        employeeId: item.employee_id,
        startDate: item.start_date,
        endDate: item.end_date,
      }));

      const payrollResponse = rawPayroll.map((item: any) => ({
        ...item,
        employeeId: item.employee_id,
      }));

      const timeTrackingResponse = rawTimeTracking.map((item: any) => ({
        ...item,
        employeeId: item.employee_id,
        clockIn: item.clock_in,
        clockOut: item.clock_out,
        totalHours: item.total_hours,
      }));

      const team = (teamResponse as any[]).map((emp) => ({
        id: emp.id,
        name: emp.name,
        role: emp.role,
        hoursWorked: emp.hours_worked,
      }));

      const uniqueTeam = Array.from(new Map(team.map(emp => [emp.id, emp])).values());

      setData({
        teamMembers: uniqueTeam,
        leaveRequests: leaveResponse,
        payroll: payrollResponse,
        timeTracking: timeTrackingResponse,
      });
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const getEmployeeName = (id?: string | number) => {
    if (!id || !data?.teamMembers) return 'Unknown';
    const emp = data.teamMembers.find(e => String(e.id) === String(id));
    return emp?.name?.trim() || `Employee (ID: ${id})`;
  };

  const handleDeleteLeave = async (id: string) => {
    try {
      await leaveService.deleteLeave(id);
      fetchDashboardData();
    } catch (error) {
      console.error('Error deleting leave request:', error);
    }
  };

  const handleDeleteTeamMember = async (id: string) => {
    try {
      await teamService.deleteTeamMember(id);
      fetchDashboardData();
    } catch (error) {
      console.error('Error deleting team member:', error);
    }
  };

  const handleDeletePayroll = async (id: string) => {
    try {
      await payrollService.deletePayroll(id);
      fetchDashboardData();
    } catch (error) {
      console.error('Error deleting payroll entry:', error);
    }
  };

  const handleDeleteTimeTracking = async (id: string) => {
    try {
      await timeTrackingService.deleteTimeTracking(id);
      fetchDashboardData();
    } catch (error) {
      console.error('Error deleting time tracking entry:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-gray-900 dark:text-gray-100">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

          {/* Team Members */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Team Members</h2>
              <button
                onClick={() => setShowTeamModal(true)}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
              >
                + Add Team Member
              </button>
            </div>
            <div className="space-y-4">
              {data?.teamMembers.map((member) => (
                <div key={member.id} className="flex items-center justify-between border-b pb-2">
                  <div>
                  <p className="font-medium text-sm">
                    <span className="text-xs text-gray-400">{member.id}</span> – {member.name}
                  </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{member.role}</p>
                    <p className="text-xs text-gray-400">Hours worked: {member.hoursWorked}</p>
                  </div>
                  <button
                    onClick={() => handleDeleteTeamMember(member.id)}
                    className="text-xs text-red-500 hover:underline"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Leave Requests */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Leave Requests</h2>
              <button
                onClick={() => setShowLeaveModal(true)}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
              >
                + Add Leave
              </button>
            </div>
            <div className="space-y-4">
              {data?.leaveRequests.map((leave) => (
                <div key={leave.id} className="border-b border-gray-200 dark:border-gray-700 pb-4 last:border-0">
                  {leave.startDate && leave.endDate && !isNaN(Date.parse(leave.startDate)) && !isNaN(Date.parse(leave.endDate)) ? (
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      {getEmployeeName(leave.employeeId)} is on leave from{' '}
                      {new Date(leave.startDate).toLocaleDateString()} to{' '}
                      {new Date(leave.endDate).toLocaleDateString()}
                    </p>
                  ) : (
                    <p className="text-sm text-red-500">
                      Invalid leave data for {getEmployeeName(leave.employeeId)}
                    </p>
                  )}
                  <div className="flex items-center justify-between mt-1">
                    <span className="text-xs text-gray-400">{leave.status}</span>
                    <button
                      onClick={() => handleDeleteLeave(leave.id)}
                      className="text-xs text-red-500 hover:underline ml-4"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Payroll */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Payroll</h2>
              <button
                onClick={() => setShowPayrollModal(true)}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
              >
                + Add Payroll
              </button>
            </div>
            <div className="space-y-4">
              {data?.payroll.map((payroll) => (
                <div key={payroll.id} className="border-b border-gray-200 dark:border-gray-700 pb-4 last:border-0 flex justify-between items-center">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      {getEmployeeName(payroll.employeeId)} earned ${payroll.salary} this month.
                    </p>
                    <span className="text-xs text-gray-400">Deductions: ${payroll.deductions}</span>
                  </div>
                  <button
                    onClick={() => handleDeletePayroll(payroll.id)}
                    className="text-xs text-red-500 hover:underline"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Time Tracking */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Time Tracking</h2>
              <button
                onClick={() => setShowTimeTrackingModal(true)}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
              >
                + Add Entry
              </button>
            </div>
            <div className="space-y-4">
              {data?.timeTracking.map((entry) => (
                <div key={entry.id} className="border-b border-gray-200 dark:border-gray-700 pb-4 last:border-0 flex justify-between items-center">
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      {getEmployeeName(entry.employeeId)} clocked in at{' '}
                      {new Date(entry.clockIn).toLocaleTimeString()} and out at{' '}
                      {new Date(entry.clockOut).toLocaleTimeString()}.
                    </p>
                    <span className="text-xs text-gray-400">Total Hours: {entry.totalHours}</span>
                  </div>
                  <button
                    onClick={() => handleDeleteTimeTracking(entry.id)}
                    className="text-xs text-red-500 hover:underline"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modals */}
        {showLeaveModal && (
          <CreateLeaveModal
            onClose={() => setShowLeaveModal(false)}
            onCreated={() => {
              setShowLeaveModal(false);
              fetchDashboardData();
            }}
          />
        )}

        {showTeamModal && (
          <CreateTeamMemberModal
            onClose={() => setShowTeamModal(false)}
            onCreated={() => {
              setShowTeamModal(false);
              fetchDashboardData();
            }}
          />
        )}

        {showPayrollModal && (
          <CreatePayrollModal
            onClose={() => setShowPayrollModal(false)}
            onCreated={() => {
              setShowPayrollModal(false);
              fetchDashboardData();
            }}
          />
        )}

        {showTimeTrackingModal && (
          <CreateTimeTrackingModal
            onClose={() => setShowTimeTrackingModal(false)}
            onCreated={() => {
              setShowTimeTrackingModal(false);
              fetchDashboardData();
            }}
          />
        )}
      </div>
    </div>
  );
};