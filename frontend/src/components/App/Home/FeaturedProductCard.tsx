import { Box, Button, Heading, Text } from "@chakra-ui/react";
import Link from "next/link";
import { useState } from "react";
import { ProductInterface } from "@/interfaces/Product";
import { CatalogueProductImages } from "@/components/App/Catalogue/ProductCard/Images";
import {
  CameraImageFromMaterials,
  setInitialMaterials,
} from "@/utils/Product/Materials";
import { SelectedMaterialsInterface } from "@/interfaces/Materials";

interface FeaturedProductCardProps {
  product: ProductInterface;
  isLarge?: boolean;
}

const FeaturedProductCard = ({
  product,
  isLarge = false,
}: FeaturedProductCardProps) => {
  const [selectedMaterials] = useState<SelectedMaterialsInterface>({
    ...setInitialMaterials(product.material_parts),
  });

  const images = product.camera
    ? CameraImageFromMaterials(product.camera.parts, selectedMaterials)
    : [];
  const link = `/product/${product.code}`;

  return (
    <Link href={link}>
      <Box
        position="relative"
        width="100%"
        height="100%"
        borderRadius="xl"
        overflow="hidden"
        transition="transform 0.3s ease"
        _hover={{ transform: "scale(1.03)" }}
      >
        <Box
          position="relative"
          width="100%"
          height={isLarge ? "550px" : "100%"}
          minHeight={isLarge ? "350px" : "250px"}
        >
          <CatalogueProductImages images={images} />
        </Box>
        <Box
          position="absolute"
          bottom="0"
          left="0"
          width="100%"
          bg="linear-gradient(to top, rgba(143, 33, 23, 0.7), transparent)"
          p={isLarge ? 6 : 4}
          color="white"
        >
          {isLarge && (
            <Text
              fontSize="sm"
              textTransform="uppercase"
              fontWeight="medium"
              mb={1}
            >
              Рекомендована колекція
            </Text>
          )}
          <Heading
            as={isLarge ? "h1" : "h3"}
            fontSize={
              isLarge ? { base: "2xl", md: "3xl" } : { base: "lg", md: "xl" }
            }
            fontWeight="medium"
            mb={isLarge ? 2 : 0}
          >
            {product.name}
          </Heading>
          {isLarge && (
            <>
              <Text mb={4} fontSize="lg">
                Відкрийте для себе наш фірмовий виріб
              </Text>
              <Button
                bg="white"
                color="brown.500"
                _hover={{ bg: "brown.50" }}
                borderRadius="full"
                size="md"
              >
                Детальніше
              </Button>
            </>
          )}
        </Box>
      </Box>
    </Link>
  );
};

export default FeaturedProductCard; 