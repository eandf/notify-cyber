// this is a custom react hook that wraps useState and keeps a copy of the
// state variable in browser local storage.

// the function has been made generic, so it will accept single values or arrays of any type

// if validationString is passed, it is stored with the value in local storage
// on future updates to the variable, the value will only be read from local
// storage if the passed validationString matches the validationString
// in local storage

// the logic here is a bit complicated, so I would ask chatGPT for an
// explanation if you're having trouble understanding it

import { useEffect, useState } from "react";

// this is used to check if T is a single value or and array of values
type SingleValue<T> = T extends Array<infer U> ? U : T;

export default function useLocalStorage<T>(
  key: string,
  initialValue: T,
  allowedValues: Array<SingleValue<T>> = [],
  validationString?: string
): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;

    try {
      const item = window.localStorage.getItem(key);
      if (!item) return initialValue;

      const parsedItem = JSON.parse(item);
      if (
        typeof parsedItem === "object" &&
        parsedItem !== null &&
        "value" in parsedItem &&
        (validationString === undefined ||
          ("validationString" in parsedItem &&
            validationString === parsedItem.validationString))
      ) {
        if (Array.isArray(parsedItem.value)) {
          return parsedItem.value.filter((v: SingleValue<T>) =>
            allowedValues.includes(v)
          ) as T;
        } else if (allowedValues.includes(parsedItem.value as SingleValue<T>)) {
          return parsedItem.value;
        }
      }
      return initialValue;
    } catch (error) {
      console.log(error);
      return initialValue;
    }
  });

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      let toStore;
      if (Array.isArray(storedValue)) {
        toStore = storedValue.filter((v: SingleValue<T>) =>
          allowedValues.includes(v)
        );
      } else if (allowedValues.includes(storedValue as SingleValue<T>)) {
        toStore = storedValue;
      }
      const serializedValue = JSON.stringify({
        value: toStore,
        validationString: validationString,
      });
      window.localStorage.setItem(key, serializedValue);
    } catch (error) {
      console.log(error);
    }
  }, [key, storedValue, allowedValues, validationString]);

  return [storedValue, setStoredValue];
}
