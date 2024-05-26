import {
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
} from "@chakra-ui/react";
import { Field } from "formik";
import * as React from "react";

/// FormField wraps simple form input fields with Chakra-ui styling
/// and the formik input component.
/// Only use this component inside of formik form component

interface IErrorHandling {
  validate: Function;
  error: string | undefined;
}

interface Props {
  id: string;
  label: string;
  required: boolean;
  type?: string;
  errorHandling?: IErrorHandling;
  variant?: string;
}

const FormField = (props: Props) => {
  let validate: Function | undefined = undefined;
  if (props.errorHandling !== undefined) {
    validate = props.errorHandling.validate;
  }
  return (
    <FormControl>
      <FormLabel htmlFor={props.id}>{props.label}</FormLabel>
      <Field
        as={Input}
        id={props.id}
        name={props.id}
        type={props.type ? props.type : "Text"}
        variant={props.variant === undefined ? "filled" : props.variant}
        validate={validate}
        required={props.required}
      />
      {validate === undefined ? (
        <></>
      ) : (
        <FormErrorMessage>{props.errorHandling?.error}</FormErrorMessage>
      )}
    </FormControl>
  );
};

export default FormField;
