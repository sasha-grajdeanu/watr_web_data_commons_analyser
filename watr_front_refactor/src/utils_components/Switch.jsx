import { Switch } from "@headlessui/react";

const SwitchDisplay = ({ checked, onChange, name_one, name_two }) => {
  return (
    <div className="flex items-center space-x-3">
        <span
          className={`text-sm font-medium ${
            !checked ? "text-watr-500" : "text-watr-100"
          }`}
        >
          {name_one}
        </span>
        <Switch
          checked={checked}
          onChange={onChange}
          className="group relative flex h-7 w-14 cursor-pointer rounded-full bg-white/10 p-1 transition-colors duration-200 ease-in-out focus:outline-none 
        data-[focus]:outline-1 data-[focus]:outline-white data-[checked]:bg-white/10"
        >
          <span
            aria-hidden="true"
            className="pointer-events-none inline-block size-5 translate-x-0 rounded-full bg-white ring-0 shadow-lg transition duration-200 ease-in-out 
          group-data-[checked]:translate-x-7"
          />
        </Switch>
        <span
          className={`text-sm font-medium ${
            checked ? "text-watr-500" : "text-watr-100"
          }`}
        >
          {name_two}
        </span>
      </div>
  );
};

export default SwitchDisplay;
