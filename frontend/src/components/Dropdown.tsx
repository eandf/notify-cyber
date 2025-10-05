// this react component renders a dropdown

// the dropdonw can contain an arbitrary react component passed in as the  content parameter.

// activeDropDownID and setActiveDropDownID allow you to have multiple dropdowns
// while only allowing one to be open at a time

import { ChevronDownIcon, ChevronUpIcon } from "@/src/components/svg";
import { useOutsideClickListener } from "@/src/hooks";
import styles from "@/src/styles/Dropdown.module.css";

type DropdownProps = {
  id: number;
  activeDropdownId: number;
  setActiveDropdownId: (id: number) => void;
  label: string;
  content: React.ReactNode;
};

export default function Dropdown({
  id,
  activeDropdownId,
  setActiveDropdownId,
  label,
  content: Content,
}: DropdownProps) {
  const dropdownRef = useOutsideClickListener<HTMLDivElement>(() => {
    setActiveDropdownId(-1);
  }, []);

  return (
    <div className={styles.container} ref={dropdownRef}>
      <button
        className={styles.button}
        onClick={() => {
          id !== activeDropdownId
            ? setActiveDropdownId(id)
            : setActiveDropdownId(-1);
        }}
      >
        <div className={styles.label}>{label}</div>
        {id == activeDropdownId ? (
          <ChevronUpIcon style={{ fontSize: "1.8em" }} />
        ) : (
          <ChevronDownIcon style={{ fontSize: "1.8em" }} />
        )}
      </button>
      {id === activeDropdownId ? (
        <div className={styles.panel}>{Content}</div>
      ) : null}
    </div>
  );
}
