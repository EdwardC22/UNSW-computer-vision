import { AddIcon, EditIcon } from "@chakra-ui/icons";
import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Button,
  Grid,
  Heading,
  useDisclosure,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { createDFormObject } from "../utils/data";
import { apiCall } from "../utils/helpers";
import EditableItemCard from "./EditableItemCard";
import FormField from "./FormField";
import ItemForm from "./ItemForm";
import PopupForm from "./PopupForm";
import "../draggable.css";

/// Component used to handle categories of a menu that can be dragged and dropped
/// to modify the order shown to customers.
/// Drag and drop of the child is handlded by the parent, the dashboard component
/// handles D&D of this editable category, and each category handles the
/// D&D of its children

interface Props {
  cId: number;
  items: Array<DItem>;
  name: string;
  deleteButton: any;
  getMenu: Function;
  handleDrag: any;
  handleDrop: any;
  setItemDrag: any;
}

// Will need to contextualise for manager and customer
const EditableCategory = ({
  name,
  items,
  deleteButton,
  cId,
  getMenu,
  handleDrag,
  handleDrop,
  setItemDrag,
}: Props) => {
  let { restaurantName } = useParams();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [formState, setFormState] = useState<DPopupFormState | undefined>(
    undefined
  );

  const [currDrag, setCurrDrag] = useState<number | undefined>(undefined);
  function handleItemDrag(ev: any, key: number) {
    // Whenever an item is dragged remember its id
    setItemDrag(key);
    setCurrDrag(key); // key is the id of the category
  }
  function handleItemDrop(ev: any, cid: number) {
    // When an item is dropped find the id of the item it was dropped ontop of
    const dragBox = items.find((item) => item.id === currDrag);
    const dropBox = items.find(
      (item) =>
        item.id ===
        parseInt(
          ev.currentTarget.id.substring(
            ev.currentTarget.id.lastIndexOf("i") + 1
          )
        )
    );

    if (!dragBox || !dropBox) return;
    if (dragBox.id !== dropBox.id) {
      apiCall(
        `/${restaurantName}/edititempos/${dragBox.id}`,
        {
          new_position: dropBox.category_pos,
        },
        "PUT"
      )
        .then((_) => getMenu())
        .catch((err: any) =>
          alert(`Error updating items position: ${err.error}`)
        );
    }
  }
  const [addForm, setAddForm] = useState<boolean>(false);

  function addItem() {
    setAddForm(true);
    onOpen();
  }
  function editCategory() {
    setAddForm(false);
    setFormState(
      createDFormObject(
        `Editing ${name}`,
        { newName: "" },
        [
          <FormField
            key={"CategoryName"}
            id="newCategoryName"
            label="Enter new category name: "
            required={true}
          />,
        ],
        (values: any) => {
          if (values.newCategoryName.trim().length === 0) {
            alert("Category name cannot be empty");
            return;
          }
          apiCall(
            `/${restaurantName}/editcategory/${cId}`,
            {
              name: values.newCategoryName,
            },
            "PUT"
          )
            .then((_) => {
              getMenu();
              onClose();
            })
            .catch((err) => alert(`Error adding new category: ${err.error}`));
        },
        deleteButton,
        onClose
      )
    );
    onOpen();
  }
  return (
    <AccordionItem
      borderWidth="1px"
      borderRadius={"md"}
      paddingTop="5px"
      marginBottom={1}
    >
      <div
        draggable
        onDragOver={(ev) => {
          ev.preventDefault();
        }}
        onDragStart={(ev) => handleDrag(ev, cId)}
        onDrop={handleDrop}
        id={`c${cId}`}
        className="draggable"
      >
        <Box
          flex="1"
          flexDirection={"row"}
          display="flex"
          justifyContent={"space-between"}
        >
          <Heading>{name}</Heading>
          <Box display="flex" flexDir="row">
            <Box display={"flex"} gap={"5px"}>
              <Button
                rightIcon={<AddIcon />}
                colorScheme={"teal"}
                onClick={addItem}
              >
                Add Item
              </Button>
              <Button
                rightIcon={<EditIcon />}
                onClick={editCategory}
                colorScheme={"purple"}
              >
                Edit Category
              </Button>
            </Box>
            <AccordionButton width="40px" paddingRight="30px">
              <AccordionIcon />
            </AccordionButton>
          </Box>
        </Box>
      </div>
      {items.length > 0 && (
        <AccordionPanel
          display="flex"
          flexDir="column"
          gap="20px"
          paddingTop="10px"
        >
          <Grid
            templateColumns={"repeat(auto-fill, minmax(200px, 1fr))"}
            gap={6}
          >
            {items.map((item) => (
              <EditableItemCard
                item={item}
                catID={cId}
                getMenu={getMenu}
                key={`${cId}${item.id}`}
                handleDrag={handleItemDrag}
                handleDrop={handleItemDrop}
              />
            ))}
          </Grid>
          <Box display={"flex"} justifyContent="flex-end"></Box>
        </AccordionPanel>
      )}
      {isOpen && !addForm ? (
        <PopupForm handleClose={onClose} open={isOpen} formState={formState} />
      ) : (
        <ItemForm
          handleClose={onClose}
          open={isOpen}
          title={"Add new item"}
          item={{
            name: "",
            description: "",
            ingredients: "",
            image: "",
            cost: 0,
            id: -1,
            category_pos: -1,
            popular: false,
          }}
          buttonText={"Add item"}
          categoryID={cId}
          getMenu={getMenu}
        />
      )}
    </AccordionItem>
  );
};

export default EditableCategory;
