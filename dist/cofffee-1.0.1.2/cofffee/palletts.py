import color as c

# green tea

prim = c.color(190, 232, 194)
second = c.color(209, 255, 252)

grad = prim.return_color_grad(second, 100)

back = c.color(140, 171, 160)
text = c.color(73, 89, 84)

green_tea = c.pallet(grad, prim, second, back, back, text)

# cofffee Bean

prim = c.color(179, 69, 18, 0.5)
second = c.color(89, 42, 20)

grad = prim.return_color_grad(second, 100)

back = c.color(230, 171, 145)
text = c.color(61, 22, 4)

cofffee_bean = c.pallet(grad, prim, second, back, back, text)

# Blue Lagoon

prim = c.color(38, 201, 147)
second = c.color(45, 212, 227)

grad = prim.return_color_grad(second, 100)

back = c.color(187, 240, 225)
text = c.color(43, 92, 87)

blue_lagoon = c.pallet(grad, prim, second, back, back, text)


# Milk Shake

prim = c.color(252, 48, 79)
second = c.color(59, 176, 255)

grad = prim.return_color_grad(second, 100)

back = c.color(245, 218, 228)
text = c.color(190, 69, 121)

milk_shake = c.pallet(grad, prim, second, back, back, text)

# Planetary Punch

prim = c.color(214, 161, 255)
second = c.color(129, 240, 179)

grad = prim.return_color_grad(second, 100)

back = c.color(20, 20, 20)
text = c.color(255, 255, 255)

planetary_punch = c.pallet(grad, prim, second, back, back, text)
