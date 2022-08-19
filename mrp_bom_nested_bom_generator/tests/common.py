from odoo.tests import Form, common


class TestNestedBomCase(common.TransactionCase):
    def setUp(self):
        super(TestNestedBomCase, self).setUp()
        MrpBom = self.env["mrp.bom"]
        ProductAttribute = self.env["product.attribute"]
        ProductAttributeValue = self.env["product.attribute.value"]
        ProductTemplate = self.env["product.template"]

        self.product_attribute_size = ProductAttribute.create({"name": "Size"})
        self.product_attribute_size_medium = ProductAttributeValue.create(
            {
                "name": "Medium",
                "attribute_id": self.product_attribute_size.id,
            }
        )
        self.product_attribute_size_large = ProductAttributeValue.create(
            {
                "name": "Large",
                "attribute_id": self.product_attribute_size.id,
            }
        )

        self.product_attribute_custom = ProductAttribute.create({"name": "Custom"})
        self.product_attribute_custom_1 = ProductAttributeValue.create(
            {
                "name": "Custom #1",
                "attribute_id": self.product_attribute_custom.id,
            }
        )
        self.product_attribute_custom_2 = ProductAttributeValue.create(
            {
                "name": "Custom #2",
                "attribute_id": self.product_attribute_custom.id,
            }
        )

        self.product_template_wood = ProductTemplate.create(
            {
                "name": "Wood",
            }
        )

        product_template = Form(ProductTemplate)
        product_template.name = "Pinocchio"
        with product_template.attribute_line_ids.new() as pta:
            pta.attribute_id = self.product_attribute_size
            pta.value_ids.add(self.product_attribute_size_medium)
            pta.value_ids.add(self.product_attribute_size_large)
        self.product_template_pinocchio = product_template.save()

        mrp_bom = Form(MrpBom)
        mrp_bom.product_tmpl_id = self.product_template_pinocchio
        mrp_bom.nested_bom = True
        with mrp_bom.nested_bom_ids.new() as nested:
            nested.product_qty = 3
            nested.attribute_ids.add(self.product_attribute_size)
        with mrp_bom.nested_bom_ids.new() as nested:
            nested.product_qty = 2
            nested.attribute_ids.add(self.product_attribute_size)

        with mrp_bom.nested_bom_ids.new() as nested:
            nested.product_tmpl_id = self.product_template_wood
            nested.product_qty = 1
        self.mrp_bom_pinocchio = mrp_bom.save()

        product_template_mrp = Form(self.env["product.template"])
        product_template_mrp.name = "Pinocchio"
        with product_template_mrp.attribute_line_ids.new() as pta:
            pta.attribute_id = self.product_attribute_size
            pta.value_ids.add(self.product_attribute_size_medium)
            pta.value_ids.add(self.product_attribute_size_large)
        self.product_template_pinocchio_mrp = product_template_mrp.save()

        self.mrp_bom_pinocchio_mrp = MrpBom.create(
            {
                "product_tmpl_id": self.product_template_pinocchio_mrp.id,
                "nested_bom": True,
            }
        )

        product_template_wand = Form(self.env["product.template"])
        product_template_wand.name = "Wand"
        with product_template_wand.attribute_line_ids.new() as pta:
            pta.attribute_id = self.product_attribute_custom
            pta.value_ids.add(self.product_attribute_custom_1)
            pta.value_ids.add(self.product_attribute_custom_2)
        self.product_template_wand = product_template_wand.save()

        self.mrp_nested_bom_line_wood = self.env["mrp.nested.bom.line"].create(
            {
                "bom_id": self.mrp_bom_pinocchio_mrp.id,
                "product_tmpl_id": self.product_template_wood.id,
                "product_qty": 3,
            }
        )
        self.mrp_nested_bom_line_wand = self.env["mrp.nested.bom.line"].create(
            {
                "bom_id": self.mrp_bom_pinocchio_mrp.id,
                "product_tmpl_id": self.product_template_wand.id,
                "product_qty": 1,
            }
        )
        self.mrp_nested_bom_line_pinocchio_2 = self.env["mrp.nested.bom.line"].create(
            {
                "bom_id": self.mrp_bom_pinocchio_mrp.id,
                "product_qty": 1,
            }
        )

    def get_product(self, id_):
        return self.env["product.template"].browse(id_)
