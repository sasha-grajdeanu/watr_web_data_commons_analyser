import React, { useEffect, useRef, useState } from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const StatisticsCard = ({ data }) => {
  const chartRef = useRef(null);
  const [customLegend, setCustomLegend] = useState("");

  const formatNumber = (num) => num.toLocaleString(undefined, { maximumFractionDigits: 3 });

  const levelLabels = Object.keys(data.level_distribution).map(level => level.replace("_", " "));
  const levelValues = Object.values(data.level_distribution);

  const pieData = {
    labels: levelLabels,
    datasets: [
      {
        data: levelValues,
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
    },
  };
  useEffect(() => {
    if (chartRef.current) {
      setCustomLegend(chartRef.current?.legend?.legendItems || []);
    }
  }, [data]);

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 w-full mx-auto flex flex-col md:flex-row items-center justify-between">
      <div className="w-full md:w-1/2 min-md:mr-4">
        <h2 className="text-xl font-bold text-gray-700 mb-4">Statistics</h2>
        <div className="flex justify-between border-b pb-2">
          <span className="text-gray-500">Depth Average:</span>
          <span className="font-semibold">{formatNumber(data.depth_average)}</span>
        </div>
        <div className="flex justify-between border-b pb-2">
          <span className="text-gray-500">Max Level:</span>
          <span className="font-semibold">{formatNumber(data.max_level)}</span>
        </div>
        <div className="flex justify-between border-b pb-2">
          <span className="text-gray-500">Min Level:</span>
          <span className="font-semibold">{formatNumber(data.min_level)}</span>
        </div>
        <h3 className="md:flex hidden text-lg font-semibold text-gray-700 mt-4">Legend</h3>
        <div className="md:flex hidden flex-wrap justify-around mt-4 w-full">
          {customLegend.length > 0 &&
            customLegend.map((item, index) => (
              <div key={index} className="flex items-center mx-2">
                <span
                  className="w-4 h-4 mr-2 inline-block rounded-full"
                  style={{ backgroundColor: item.fillStyle }}
                ></span>
                <span className="text-gray-700 text-sm">{item.text}</span>
              </div>
            ))}
        </div>
      </div>
      <div className="w-full md:w-1/2 flex flex-col">
        <h3 className="text-lg font-semibold text-gray-700 mb-2 max-md:mt-4">Level Distribution</h3>
        <div className="w-full h-60 sm:h-80 md:h-96 lg:h-[400px] flex justify-center">
          <Pie ref={chartRef} data={pieData} options={pieOptions} />
        </div>
        {/* Custom Legend */}
        <div className="flex md:hidden flex-wrap justify-center mt-4">
          {customLegend.length > 0 &&
            customLegend.map((item, index) => (
              <div key={index} className="flex items-center mx-2">
                <span
                  className="w-4 h-4 mr-2 inline-block rounded-full"
                  style={{ backgroundColor: item.fillStyle }}
                ></span>
                <span className="text-gray-700 text-sm">{item.text}</span>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default StatisticsCard;
