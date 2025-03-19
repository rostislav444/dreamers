import { Box, Grid, Flex, Text, Image } from "@chakra-ui/react";
import { SelectedMaterialsInterface } from "@/interfaces/Materials";
import { ProductPart } from "@/interfaces/Product/Parts";
import { ChevronUpIcon } from "@chakra-ui/icons";
import { useState } from "react";
import { BASE_URL, MEDIA_LOCAL } from "@/local";
import { useRouter } from "next/router";

interface MaterialItemProps {
  material: any;
  isSelected: boolean;
  isCatalog: boolean;
  onClick: () => void;
}

const MaterialItem = ({
  material,
  isSelected,
  isCatalog,
  onClick,
}: MaterialItemProps) => (
  <Box>
    <Box
      position="relative"
      display="inline-block"
      p="2px"
      m={isCatalog ? "0" : "0 0 0 2px"}
      borderWidth="2px"
      borderColor={isSelected ? "brown.500" : "transparent"}
      borderRadius="4px"
      cursor="pointer"
      _hover={{ borderColor: "orange.500" }}
      onClick={onClick}
    >
      {material?.material?.color && (
        <Box
          w={isCatalog ? "20px" : "24px"}
          h={isCatalog ? "20px" : "24px"}
          borderRadius="3px"
          bg={material.material.color.hex}
        />
      )}
      {material?.material?.image && (
        <Box
          w={isCatalog ? "20px" : "24px"}
          h={isCatalog ? "20px" : "24px"}
          borderRadius="3px"
        >
          <Image
            w="100%"
            h="100%"
            src={
              MEDIA_LOCAL
                ? BASE_URL + material.material.image
                : material.material.image
            }
            alt={material.id.toString()}
          />
        </Box>
      )}
    </Box>
  </Box>
);

interface UniversalMaterialsProps {
  parts: ProductPart[];
  selectedMaterials: SelectedMaterialsInterface;
  setSelectedMaterials: (materials: SelectedMaterialsInterface) => void;
  isCatalog?: boolean;
  mobile?: boolean;
}

export const UniversalMaterials = ({
  parts,
  selectedMaterials,
  setSelectedMaterials,
  isCatalog = false,
  mobile = false,
}: UniversalMaterialsProps) => {
  const router = useRouter();

  const validParts = parts.filter(
    (part) =>
      part.material_groups.length >= 1 &&
      part.material_groups.some((group) => group.materials.length > 0),
  );

  const [showAll, setShowAll] = useState<boolean[]>(validParts.map(() => true));

  const getFlatMaterials = (part: ProductPart) => {
    return part.material_groups.flatMap((group) =>
      group.materials.map((material) => ({
        ...material,
        groupName: group.name,
      })),
    );
  };

  const handleMaterialsSet = (part: any, groupName: string, material: any) => {
    const newMaterials = {
      ...selectedMaterials,
      [part.blender_name]: {
        partId: part.id,
        group: groupName,
        material: material.id,
        material_name: material.name,
      },
    };

    setSelectedMaterials(newMaterials);

    if (!isCatalog) {
      const materialsSlug = Object.values(newMaterials)
        .map((material: any) => material.partId + "-" + material.material)
        .join("_");

      const { slug } = router.query as { slug: string[] };
      router.push(
        {
          pathname: router.pathname,
          query: { slug: [slug[0], materialsSlug] },
        },
        router.pathname,
        { shallow: true },
      );
    }
  };

  if (validParts.length === 0) return null;

  return (
    <Box>
      {!isCatalog && (
        <Text fontSize="xl" fontWeight="bold">
          Колір
        </Text>
      )}
      {validParts.map((part, i) => (
        <Box key={part.id}>
          <Flex
            justifyContent="space-between"
            alignItems="center"
            onClick={() =>
              !isCatalog &&
              setShowAll((old) => {
                const newShowAll = [...old];
                newShowAll[i] = !old[i];
                return newShowAll;
              })
            }
            mt="2"
          >
            <Text fontSize="md">{part.name}</Text>
            {!isCatalog && (
              <ChevronUpIcon
                w="6"
                h="6"
                color="brown.500"
                cursor="pointer"
                transform={showAll[i] ? "rotate(180deg)" : "rotate(0deg)"}
              />
            )}
          </Flex>

          {(showAll[i] || isCatalog) && (
            <Box>
              {isCatalog ? (
                <Grid
                  mt={1}
                  mb={1}
                  gridTemplateColumns="repeat(auto-fill, 34px)"
                  gap={1}
                >
                  {getFlatMaterials(part).map((material) => (
                    <MaterialItem
                      key={material.id}
                      material={material}
                      isSelected={
                        selectedMaterials[part.blender_name]?.material ===
                        material.id
                      }
                      isCatalog={isCatalog}
                      onClick={() =>
                        handleMaterialsSet(part, material.groupName, material)
                      }
                    />
                  ))}
                </Grid>
              ) : (
                part.material_groups.map(
                  (group) =>
                    group.materials.length > 0 && (
                      <Box key={group.id}>
                        <Text fontSize="sm" mt={1} color="orange.500">
                          {group.name}
                        </Text>
                        <Grid
                          mt={1}
                          ml="-5px"
                          mb={1}
                          gridTemplateColumns="repeat(auto-fill, 34px)"
                          gap={1}
                        >
                          {group.materials.map((material) => (
                            <MaterialItem
                              key={material.id}
                              material={material}
                              isSelected={
                                selectedMaterials[part.blender_name]
                                  ?.material === material.id
                              }
                              isCatalog={isCatalog}
                              onClick={() =>
                                handleMaterialsSet(part, group.name, material)
                              }
                            />
                          ))}
                        </Grid>
                      </Box>
                    ),
                )
              )}
            </Box>
          )}
        </Box>
      ))}
    </Box>
  );
};
