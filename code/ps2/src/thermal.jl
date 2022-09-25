export temperature

function temperature(particles::Particles)
    velocities = map(particles) do particle
        particle.v
    end
    n = length(particles)
    return 16 / n * sum(abs2, velocities)
end

volume(particles) = length(particles) / ρ
