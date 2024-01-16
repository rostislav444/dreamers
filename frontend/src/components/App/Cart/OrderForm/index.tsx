import {Box, Button, FormControl, FormErrorMessage, Grid, GridItem, Heading, useMediaQuery} from "@chakra-ui/react";
import {SubmitHandler, useForm} from "react-hook-form";
import {CustomInput, CustomTextarea} from "./style";
import fetchApi from "@/utils/fetch";
import {useCart} from "@/context/Cart";

interface FormField {
    name: string;
    placeholder: string;
    type?: string;
    validation?: Record<string, any>;
    colSpan?: boolean;
}

const formFields: FormField[] = [
    {name: "first_name", colSpan: true, placeholder: "Імʼя *", validation: {required: "Поле обовʼязково до заповнення"}},
    {name: "last_name", placeholder: "Фамілія *", validation: {required: "Поле обовʼязково до заповнення"}},
    {name: "father_name", placeholder: "По батькові"},
    {name: "email", placeholder: "E-mail", type: "email", validation: {pattern: {value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i, message: "Неверный формат email"}}},
    {name: "phone", placeholder: "Номер телефону *", validation: {required: "Поле обовʼязково до заповнення"}},
    {name: "city", placeholder: "Місто", validation: {required: "Вкажіть місто"}},
    {name: "address", placeholder: "Адреса / Відділеня нової пошти", validation: {required: "Поле обовʼязково до заповнення"}},
    {name: "comment", type: 'textarea', colSpan: true, placeholder: "Коментар до замовлення"},
];

interface FormData {
    [key: string]: string;
}

export const OrderForm = () => {
    const api = fetchApi('uk')
    const {cart} = useCart();
    const [mobile] = useMediaQuery('(max-width: 1367px)');
    const {
        handleSubmit,
        register,
        formState: {errors},
    } = useForm<FormData>();

    const onSubmit: SubmitHandler<FormData> = async (data) => {
        const items = cart.map(item => ({sku: item.sku, price: item.price, quantity: item.qty}))
        const payload = {...data, items}

        console.log(payload)

        const response = await api.post('/order/', payload)
        if (response.ok) {
            console.log(response)
        }
    };

    return (
        <Box>
            <Heading size="lg" mb={8}>Оформити замовлення</Heading>
            <form onSubmit={handleSubmit(onSubmit)}>
                <Grid templateColumns={mobile ? '1fr' : '1fr 1fr'} gap={4}>
                    {formFields.map((field) => (
                        <GridItem key={field.name} colSpan={field.colSpan ? (mobile ? 1 : 2) : 1}>
                            {field.type === 'textarea' ? (
                                    <CustomTextarea
                                        placeholder={field.placeholder} {...register(field.name, field.validation)} />
                                ) :
                                <FormControl isInvalid={!!errors[field.name]?.message}>
                                    <CustomInput
                                        placeholder={field.placeholder}
                                        type={field.type}
                                        {...register(field.name, field.validation)}
                                    />
                                    <FormErrorMessage>{errors[field.name]?.message}</FormErrorMessage>
                                </FormControl>
                            }
                        </GridItem>
                    ))}
                </Grid>
                <Button w="100%" p={8} type="submit" mt={4} colorScheme="teal">
                    Підтвердити замовлення
                </Button>
            </form>

            <FormErrorMessage>{errors.comments?.message}</FormErrorMessage>
        </Box>
    );
};
