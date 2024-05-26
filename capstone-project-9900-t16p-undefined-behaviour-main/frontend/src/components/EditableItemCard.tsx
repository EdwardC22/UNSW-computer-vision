import { Button, useDisclosure } from "@chakra-ui/react";
import ItemForm from "./ItemForm";
import { apiCall } from "../utils/helpers";
import { useParams } from "react-router-dom";
import { EditIcon } from "@chakra-ui/icons";
import ItemCard from "./ItemCard";
import DeleteButton from "./DeleteButton";

/// EditableItemCard wraps a generic item display in the ability to be dragged
/// and dropped, as well as handles all changing of its own data.
interface Props {
  item: DItem;
  catID: number;
  getMenu: Function;
  handleDrop: any;
  handleDrag: any;
}
const EditableItemCard = ({
  item,
  catID,
  getMenu,
  handleDrag,
  handleDrop,
}: Props) => {
  let { restaurantName } = useParams();
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <div
      draggable
      onDragOver={(ev) => ev.preventDefault()}
      onDragStart={(ev) => handleDrag(ev, item.id)}
      onDrop={(ev) => handleDrop(ev, catID)}
      id={`i${item.id}`}
      className="draggable"
    >
      <ItemCard
        item={item}
        catID={catID}
        action={
          <Button
            onClick={onOpen}
            colorScheme="purple"
            alignSelf={"flex-end"}
            rightIcon={<EditIcon />}
          >
            Edit Item
          </Button>
        }
      />
      {isOpen && (
        <ItemForm
          handleClose={onClose}
          item={item}
          open={isOpen}
          title={"Edit Item"}
          buttonText={"Save changes"}
          deleteButton={
            <DeleteButton
              clickHandler={() => {
                apiCall(
                  `/${restaurantName}/deleteitem/${item.id}`,
                  {},
                  "DELETE"
                )
                  .then(() => {
                    getMenu();
                    onClose();
                  })
                  .catch((err: any) =>
                    alert(`Error deleting item: ${err.error}`)
                  );
              }}
            />
          }
          categoryID={catID}
          getMenu={getMenu}
        />
      )}
    </div>
  );
};

export default EditableItemCard;
