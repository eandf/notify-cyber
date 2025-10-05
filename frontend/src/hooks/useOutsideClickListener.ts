// this is a custom react hook that detects clicks outside the boundaries of an
// html element and calls function
// ignoreClicksIn is a list of html elements that do not count as outiside,
// whether or nto they are inside or outside of the target element

import { RefObject, useEffect, useRef } from "react";

const useOutsideClickListener = <T extends HTMLElement>(
  onOutsideClick: () => void,
  ignoreClicksIn: RefObject<Element>[]
): RefObject<T> => {
  const ref = useRef<T | null>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        let isIgnored = false;

        if (ignoreClicksIn) {
          isIgnored = ignoreClicksIn.some(
            (ignoredRef) =>
              ignoredRef.current &&
              ignoredRef.current.contains(event.target as Node)
          );
        }

        if (!isIgnored) {
          onOutsideClick();
        }
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [onOutsideClick, ignoreClicksIn]);

  return ref;
};

export default useOutsideClickListener;
