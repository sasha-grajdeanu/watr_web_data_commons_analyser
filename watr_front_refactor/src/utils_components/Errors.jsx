import { FiAlertCircle } from "react-icons/fi";

const ErrorsMessage = ({ errorMessage }) => {
    return (
        <div className="text-red-500 text-md mt-1 flex flex-row gap-1 items-center">
        <FiAlertCircle className="inline" />
        <span>{errorMessage}</span>
        </div>
    );
}

export default ErrorsMessage;
