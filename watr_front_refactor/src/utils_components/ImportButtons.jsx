import { Button, Field, Fieldset } from "@headlessui/react";

const ImportButtons = ({ importFunctionalities }) => {
  return (
    <Fieldset className="flex flex-col w-full pt-2">
      {importFunctionalities.map((importFunctionality, index) => (
        <Field className="flex flex-col w-full pt-2 px-1" key={index}>
          <Button
            onClick={importFunctionality.action}
            className="rounded bg-watr-200 hover:bg-watr-100 text-xl py-2 duration-300 text-white w-full"
          >
            {importFunctionality.name}
          </Button>
        </Field>
      ))}
    </Fieldset>
  );
};

export default ImportButtons;