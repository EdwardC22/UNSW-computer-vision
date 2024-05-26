import { VStack, ModalFooter, Button, ButtonGroup } from "@chakra-ui/react";
import { Formik } from "formik";

export const createDFormObject = (
  title: string,
  initialValues: Object,
  formFields: Array<any>,
  submitHandler: Function,
  deleteButton: any | undefined,
  closeModal: Function
) => {
  return {
    title: title,
    form: (
      <Formik
        initialValues={{ categoryName: "" }}
        onSubmit={(values, actions) => submitHandler(values)}
      >
        {({ handleSubmit, errors, touched }) => (
          <form onSubmit={handleSubmit}>
            <VStack>
              <>
                {formFields}
                <ModalFooter
                  display="flex"
                  justifyContent={"space-between"}
                  width="100%"
                >
                  {deleteButton}
                  <ButtonGroup>
                    <Button colorScheme="blue" onClick={() => closeModal()}>
                      Close
                    </Button>
                    <Button colorScheme={"teal"} type={"submit"}>
                      Submit
                    </Button>
                  </ButtonGroup>
                </ModalFooter>
              </>
            </VStack>
          </form>
        )}
      </Formik>
    ),
  };
};

export const enum Timeframe {
  hourly = "hourly",
  daily = "daily",
  monthly = "monthly",
}
