import {
    Box,
    Button,
    Card,
    CardBody,
    CardFooter,
    Divider,
    Flex,
    Grid,
    Heading,
    Image,
    Stack,
    Text,
    useMediaQuery
} from "@chakra-ui/react";
import {DeleteIcon} from '@chakra-ui/icons';
import {useCart} from "@/context/Cart";
import Link from "next/link";
import {useRouter} from "next/router";
import {useEffect} from "react";
import {OrderForm} from "@/components/App/Cart/OrderForm";
import {addSpacesToNumber} from "@/utils/numbers";
import {OrderTotal} from "@/components/App/Cart/OrderTotal";
import fetchApi from "@/utils/fetch";

export const CartData = () => {
    const [mobile] = useMediaQuery('(max-width: 1367px)')
    const {cart, updateItem, removeItem, calculateTotal, calculateTotalQty} = useCart();
    const router = useRouter();

    const handleQuantityChange = (sku: number, newQty: number) => {
        updateItem(sku, newQty);
    };

    const handleRemoveItem = (sku: number) => {
        removeItem(sku);
    };

    useEffect(() => {
        if (cart.length === 0) {
            router.push('/');
        }
    }, [cart.length]);

    return (
        <Box mt={8} display='grid' gridTemplateColumns={mobile ? '1fr' : '1fr minmax(320px, 1fr)'} gap={8}>
            <Box>
                <Heading size="lg" mb={8}>Кошик</Heading>
                <Grid gridTemplateColumns='repeat(auto-fill, minmax(300px, 1fr))' gap={8}>
                    {cart.map(item =>
                        <Card key={item.sku} bg={'#ffffff85'}>
                            <CardBody>
                                <Link href={`/product/${item.code}`}>
                                    <Image src={item.image} alt={item.name + '-' + item.sku}/>
                                </Link>
                                <Stack mt='6' spacing='3'>
                                    <Heading color={'brown.500'} size='md'>{item.name}</Heading>
                                    <Flex justifyContent='space-between' alignItems='center'>
                                        <Box>
                                            <Text fontSize='2xl'>{addSpacesToNumber(item.price)} грн.</Text>
                                            {item.qty > 1 && <Text color='brown.400'
                                                                   fontSize='xs'>Cума: {addSpacesToNumber(item.price * item.qty)} грн.</Text>}
                                        </Box>
                                        <Flex justifyContent='center' alignItems='center'>
                                            <Button
                                                size='xs'
                                                as="span"
                                                onClick={() => item.qty > 1 && handleQuantityChange(item.sku, item.qty - 1)}
                                            >-</Button>
                                            <Box as='span' p={4}>{item.qty}</Box>
                                            <Button
                                                size='xs'
                                                as="span"
                                                onClick={() => handleQuantityChange(item.sku, item.qty + 1)}
                                            >+</Button>
                                        </Flex>
                                    </Flex>
                                </Stack>
                            </CardBody>
                            <Divider borderWidth={1}/>
                            <CardFooter p={2}>
                                <Button w='100%' variant='ghost' color='brown.500'>
                                    <Flex alignItems='center' as='span'>
                                        <DeleteIcon mr={4}/>
                                        <Box onClick={() => handleRemoveItem(item.sku)} as='span'>Видалити з
                                            кошика</Box>
                                    </Flex>
                                </Button>
                            </CardFooter>
                        </Card>
                    )}
                </Grid>
                <OrderTotal mobile={mobile} calculateTotalQty={calculateTotalQty} calculateTotal={calculateTotal} />
            </Box>
            <Box>
                <OrderForm/>
            </Box>
        </Box>
    );
};
