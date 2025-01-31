export default function Spinner({ size = "8", color = "white" }) {
    return (
      <div className="flex justify-center items-center">
        <div
          className={`h-${size} w-${size} animate-spin rounded-full border-4 border-${color} border-t-transparent`}
        />
      </div>
    );
  }
  