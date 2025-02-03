const sizeClasses = {
  sm: "h-8 w-8",
  md: "h-12 w-12",
  lg: "h-16 w-16",
};

const colorClasses = {
  white: "border-white",
  watr: "border-watr-100",
};

export default function Spinner({ size = "md", color = "white" }) {
  return (
    <div className="flex justify-center items-center">
      <div
        className={`${sizeClasses[size]} ${
          colorClasses[color]
        } animate-spin rounded-full border-4 border-t-transparent`}
      />
    </div>
  );
}