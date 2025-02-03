import { FiAlertCircle } from "react-icons/fi";

const ErrorsMessage = ({ errorMessage }) => {
  return (
    <div className="text-md mt-2 flex flex-row gap-2 items-center">
      <FiAlertCircle className="inline text-red-500" />
      <span className="text-red-500">{errorMessage}</span>
    </div>
  );
};

export default ErrorsMessage;
