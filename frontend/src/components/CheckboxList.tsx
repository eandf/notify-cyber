// this react component renders a list of items with checkboxes next to them
// the component keeps a list updated with the items that are currently selected

interface CheckboxListProps {
  items: {
    name: string;
    id: string;
  }[];
  selectedItems: string[];
  setSelectedItems: (source: string, selected: boolean) => void;
}

export default function CheckboxList({
  items,
  selectedItems,
  setSelectedItems,
}: CheckboxListProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const itemID = e.target.name;
    const checked = e.target.checked;
    setSelectedItems(itemID, checked);
  };

  return (
    <>
      {/* the && means we only render if there are items in the list */}
      {items &&
        items.map((item) => (
          <div key={item.id}>
            <input
              type="checkbox"
              name={item.id}
              checked={selectedItems.includes(item.id)}
              onChange={handleChange}
            />
            <span style={{ paddingLeft: "0.5em" }}>{item.name}</span>
          </div>
        ))}
    </>
  );
}
